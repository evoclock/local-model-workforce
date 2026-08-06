#!/usr/bin/env python3
"""Validate the governed evidence envelope and its strict LMW receipts.

The repository deliberately keeps this validator dependency-free.  It implements
only the JSON Schema vocabulary used by the published contracts, then applies the
cross-field flywheel invariants that JSON Schema cannot express here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = ROOT / "schemas"
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _type_ok(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def _resolve_pointer(root: dict[str, Any], pointer: str) -> Any:
    current: Any = root
    if pointer in ("", "#"):
        return current
    for part in pointer.removeprefix("#/").split("/"):
        current = current[part.replace("~1", "/").replace("~0", "~")]
    return current


def _schema_for_ref(ref: str, current_root: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    if ref.startswith("#"):
        return _resolve_pointer(current_root, ref), current_root
    path = (SCHEMA_DIR / ref).resolve()
    if SCHEMA_DIR.resolve() not in path.parents:
        raise ValueError(f"schema reference escapes schema directory: {ref}")
    return json.loads(path.read_text()), json.loads(path.read_text())


def _validate(instance: Any, schema: dict[str, Any], root: dict[str, Any], path: str, errors: list[str]) -> None:
    if "$ref" in schema:
        try:
            target, target_root = _schema_for_ref(schema["$ref"], root)
        except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: cannot resolve {schema['$ref']}: {exc}")
            return
        _validate(instance, target, target_root, path, errors)
        return

    if "oneOf" in schema:
        branch_errors: list[list[str]] = []
        for branch in schema["oneOf"]:
            candidate: list[str] = []
            _validate(instance, branch, root, path, candidate)
            if not candidate:
                branch_errors.append([])
            else:
                branch_errors.append(candidate)
        if sum(not candidate for candidate in branch_errors) != 1:
            errors.append(f"{path}: oneOf matched {sum(not candidate for candidate in branch_errors)} branches")
            for candidate in branch_errors:
                if candidate:
                    errors.extend(candidate[:3])
        return

    expected = schema.get("type")
    if expected is not None:
        types = expected if isinstance(expected, list) else [expected]
        if not any(_type_ok(instance, item) for item in types):
            errors.append(f"{path}: expected {types}, got {type(instance).__name__}")
            return

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} is not in enum")

    if isinstance(instance, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                errors.append(f"{path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in properties:
                continue
            if additional is False:
                errors.append(f"{path}: unexpected property {key!r}")
            elif isinstance(additional, dict):
                _validate(value, additional, root, f"{path}.{key}", errors)
        for key, child_schema in properties.items():
            if key in instance:
                _validate(instance[key], child_schema, root, f"{path}.{key}", errors)
        minimum = schema.get("minProperties")
        if minimum is not None and len(instance) < minimum:
            errors.append(f"{path}: needs at least {minimum} properties")

    if isinstance(instance, list):
        minimum = schema.get("minItems")
        if minimum is not None and len(instance) < minimum:
            errors.append(f"{path}: needs at least {minimum} items")
        if schema.get("uniqueItems"):
            encoded = [_canonical(item) for item in instance]
            if len(encoded) != len(set(encoded)):
                errors.append(f"{path}: items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for index, item in enumerate(instance):
                _validate(item, item_schema, root, f"{path}[{index}]", errors)

    if isinstance(instance, str):
        minimum = schema.get("minLength")
        if minimum is not None and len(instance) < minimum:
            errors.append(f"{path}: needs at least {minimum} characters")
        pattern = schema.get("pattern")
        if pattern is not None and re.search(pattern, instance) is None:
            errors.append(f"{path}: does not match {pattern!r}")

    if isinstance(instance, (int, float)) and not isinstance(instance, bool):
        minimum = schema.get("minimum")
        if minimum is not None and instance < minimum:
            errors.append(f"{path}: must be >= {minimum}")


def _receipt_id(receipt: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical(receipt)).hexdigest()


def _safe_relative_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\x00" in value or "\\" in value:
        return False
    if Path(value).is_absolute():
        return False
    parts = value.split("/")
    return "." not in parts and ".." not in parts


def _ref_errors(values: Any, label: str) -> list[str]:
    if not isinstance(values, list):
        return []
    return [f"{label} contains unsafe artifact reference {value!r}"
            for value in values if not _safe_relative_ref(value)]


def _semantic_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_evidence = hashlib.sha256(
        _canonical({k: v for k, v in record.items() if k != "evidence_id"})
    ).hexdigest()
    if record.get("evidence_id") != expected_evidence:
        errors.append("evidence_id does not match the canonical record payload")

    receipt = record.get("receipt")
    if isinstance(receipt, dict):
        receipt_hashes = receipt.get("artifact_hashes")
        if not receipt_hashes:
            errors.append("receipt.artifact_hashes must retain at least one artifact hash")
        elif isinstance(receipt_hashes, dict):
            for name, digest in receipt_hashes.items():
                if not _safe_relative_ref(name):
                    errors.append(f"receipt artifact reference {name!r} is unsafe")
                if not isinstance(digest, str) or not _HEX64.fullmatch(digest):
                    errors.append(f"receipt artifact {name!r} must use a lowercase SHA-256 hash")
        expected_receipt = _receipt_id(receipt)
        if record.get("receipt_id") != expected_receipt:
            errors.append("receipt_id does not match the canonical receipt")
        state = record.get("state")
        semantic_status = {"passed": "passed", "failed": "failed", "denied": "failed", "timed_out": "failed", "not_run": "not_run"}.get(receipt.get("status"))
        if isinstance(state, dict) and semantic_status != state.get("semantic_status"):
            errors.append("receipt.status must map to state.semantic_status, not merely the process exit code")
        output = record.get("output")
        if isinstance(output, dict):
            output_hashes = output.get("artifact_hashes")
            output_refs = output.get("artifact_refs")
            errors.extend(_ref_errors(output_refs, "output.artifact_refs"))
            panel_ref = output.get("panel_ref")
            if not isinstance(panel_ref, str) or not _safe_relative_ref(panel_ref):
                errors.append("output.panel_ref must be a safe relative artifact reference")
            elif isinstance(output_refs, list) and panel_ref not in output_refs:
                errors.append("output.panel_ref must be listed in output.artifact_refs")
            if isinstance(output_hashes, dict) and isinstance(output_refs, list):
                for name in output_refs:
                    if name not in output_hashes:
                        errors.append(f"output artifact {name!r} has no hash")
                for name, digest in output_hashes.items():
                    if not _safe_relative_ref(name):
                        errors.append(f"output artifact reference {name!r} is unsafe")
                    if not isinstance(digest, str) or not _HEX64.fullmatch(digest):
                        errors.append(f"output artifact {name!r} must use a lowercase SHA-256 hash")
                if isinstance(receipt_hashes, dict):
                    for name in receipt_hashes:
                        if name not in output_hashes:
                            errors.append(f"receipt artifact {name!r} is not retained in output.artifact_hashes")

    state = record.get("state")
    if isinstance(state, dict):
        for state_name in ("before", "after"):
            state_part = state.get(state_name)
            if isinstance(state_part, dict):
                errors.extend(_ref_errors(state_part.get("artifact_refs"), f"state.{state_name}.artifact_refs"))
                hashes = state_part.get("artifact_hashes")
                refs = state_part.get("artifact_refs")
                if isinstance(hashes, dict) and isinstance(refs, list):
                    for name in refs:
                        if name not in hashes:
                            errors.append(f"state.{state_name} artifact {name!r} has no hash")
    lineage = record.get("lineage")
    if isinstance(lineage, dict):
        errors.extend(_ref_errors(lineage.get("artifact_refs"), "lineage.artifact_refs"))

    checks = record.get("checks")
    if not isinstance(checks, list):
        checks = []
    check_ids = [item.get("check_id") for item in checks if isinstance(item, dict)]
    if len(check_ids) != len(set(check_ids)):
        errors.append("checks.check_id values must be unique")
    for index, item in enumerate(checks):
        if not isinstance(item, dict):
            errors.append(f"checks[{index}] must be an object")
        elif not isinstance(item.get("criterion"), str) or not item.get("criterion"):
            errors.append(f"checks[{index}].criterion must be a non-empty string")
        elif not isinstance(item.get("evidence_refs"), list):
            errors.append(f"checks[{index}].evidence_refs must be an array")
    failed = [item for item in checks if isinstance(item, dict) and item.get("status") == "failed"]
    divergence = record.get("first_divergence")
    correction = record.get("correction")
    remedy = record.get("remedy")
    remedy_status = remedy.get("status") if isinstance(remedy, dict) else None
    receipt_status = record.get("receipt", {}).get("status") if isinstance(record.get("receipt"), dict) else None
    if divergence is None:
        if failed:
            errors.append("failed checks require first_divergence")
        if receipt_status in {"failed", "denied", "timed_out"}:
            errors.append("failed execution receipt requires first_divergence")
        if correction is not None:
            errors.append("correction requires first_divergence")
        if remedy is not None and remedy_status != "not_required":
            errors.append("an active remedy requires first_divergence")
    elif correction is None and (remedy is None or remedy_status == "not_required"):
        errors.append("first_divergence requires an active correction or remedy")

    verification = record.get("verification")
    if not isinstance(verification, dict):
        verification = {}
    disposition = record.get("disposition")
    if disposition == "promote":
        lineage = record.get("lineage")
        historical_divergence = (
            divergence is not None
            and remedy_status == "verified"
            and isinstance(lineage, dict)
            and bool(lineage.get("parent_evidence_ids"))
        )
        if divergence is not None and not historical_divergence:
            errors.append("promote requires no unresolved first_divergence")
        if failed:
            errors.append("promote requires every check to pass")
        if verification.get("status") != "passed":
            errors.append("promote requires passed verification")
        if remedy_status is not None and remedy_status not in {"not_required", "verified"}:
            errors.append("promote cannot retain an active remedy")
        state = record.get("state")
        if not isinstance(state, dict) or state.get("panel_status") != "sign-off":
            errors.append("promote requires panel sign-off")
    if remedy_status == "verified":
        if verification.get("status") != "passed":
            errors.append("verified remedy requires passed verification")
        lineage = record.get("lineage")
        if not isinstance(lineage, dict) or not lineage.get("parent_evidence_ids"):
            errors.append("verified remedy requires parent evidence lineage")

    verification = record.get("verification")
    if isinstance(verification, dict):
        ids = verification.get("check_ids")
        if isinstance(ids, list):
            for check_id in ids:
                if check_id not in check_ids:
                    errors.append(f"verification references unknown check {check_id!r}")
        receipt_ids = verification.get("receipt_ids")
        if isinstance(receipt_ids, list) and isinstance(record.get("receipt_id"), str):
            if record["receipt_id"] not in receipt_ids:
                errors.append("verification.receipt_ids must include receipt_id")

    output = record.get("output")
    refs = set(output.get("artifact_refs", [])) if isinstance(output, dict) and isinstance(output.get("artifact_refs"), list) else set()
    for section_name in ("tools", "checks", "correction", "first_divergence", "remedy", "verification", "lineage"):
        section = record.get(section_name)
        values: list[Any]
        if isinstance(section, list):
            values = section
        elif isinstance(section, dict):
            values = [section]
        else:
            values = []
        for item in values:
            if not isinstance(item, dict):
                continue
            evidence_refs = item.get("evidence_refs")
            if not isinstance(evidence_refs, list):
                continue
            for ref in evidence_refs:
                if ref not in refs:
                    errors.append(f"{section_name} references unretained artifact {ref!r}")
    return errors


def validate_record(record: dict[str, Any], schema_path: Path | None = None) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be a JSON object"]
    schema_path = schema_path or (SCHEMA_DIR / "evidence_record.v1.json")
    try:
        schema = json.loads(schema_path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot load evidence schema: {exc}"]
    errors: list[str] = []
    _validate(record, schema, schema, "$", errors)
    errors.extend(_semantic_errors(record))
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    args = parser.parse_args(argv)
    try:
        record = json.loads(args.record.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    if not isinstance(record, dict):
        print("FAIL: evidence record must be a JSON object")
        return 1
    errors = validate_record(record)
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        return 1
    print(f"PASS: {args.record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
