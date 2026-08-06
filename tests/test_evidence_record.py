import hashlib
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "validate_evidence_record", ROOT / "scripts" / "validate_evidence_record.py"
)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


def make_record(*, status="passed", disposition="promote", divergence=None, remedy=None):
    receipt = {
        "command_id": "fixture.verify.hard",
        "status": status,
        "exit_code": 0 if status == "passed" else 1,
        "artifact_hashes": {"ground-truth.json": "a" * 64},
        "reason_codes": [],
    }
    receipt_id = validator._receipt_id(receipt)
    record = {
        "schema_version": "1",
        "evidence_id": "0" * 64,
        "task": {
            "task_id": "fixture-task",
            "workflow_id": "fixture-workflow",
            "request": "execute the fixture",
            "contract_ref": None,
            "attempt": 1,
        },
        "state": {
            "before": None,
            "after": {
                "artifact_refs": ["ground-truth.json"],
                "artifact_hashes": {"ground-truth.json": "a" * 64},
            },
            "semantic_status": "failed" if status in {"denied", "timed_out"} else status,
            "gate_status": "failed" if status in {"denied", "timed_out"} else status,
            "panel_status": "sign-off" if status == "passed" else "revise",
        },
        "output": {
            "artifact_refs": ["ground-truth.json"],
            "artifact_hashes": {"ground-truth.json": "a" * 64},
            "panel_ref": "ground-truth.json",
        },
        "tools": [{
            "tool_id": "verify",
            "kind": "deterministic_gate",
            "command_id": "fixture.verify.hard",
            "evidence_refs": ["ground-truth.json"],
        }],
        "checks": [{
            "check_id": "R1",
            "criterion": "R1",
            "status": "failed" if status in {"denied", "timed_out"} else status,
            "evidence_refs": ["ground-truth.json"],
        }],
        "receipt_id": receipt_id,
        "receipt": receipt,
        "correction": None if divergence is None else [{
            "correction_id": "c1",
            "source": "panel",
            "criterion": "R1",
            "observed": "the criterion failed",
            "action": "rerun the corrected implementation",
            "evidence_refs": ["ground-truth.json"],
        }],
        "first_divergence": divergence,
        "remedy": remedy,
        "verification": {
            "status": "passed" if status == "passed" else "not_run",
            "check_ids": ["R1"],
            "evidence_refs": ["ground-truth.json"],
            "receipt_ids": [receipt_id],
        },
        "lineage": {
            "parent_evidence_ids": [],
            "parent_receipt_ids": [],
            "artifact_refs": ["ground-truth.json"],
        },
        "disposition": disposition,
    }
    record["evidence_id"] = hashlib.sha256(
        validator._canonical({key: value for key, value in record.items() if key != "evidence_id"})
    ).hexdigest()
    return record


class EvidenceRecordValidationTests(unittest.TestCase):
    def test_schema_is_published_with_the_existing_contracts(self):
        schema = json.loads((ROOT / "schemas" / "evidence_record.v1.json").read_text())
        self.assertEqual(schema["$id"], "evidence_record.v1.json")
        self.assertEqual(schema["properties"]["receipt"]["$ref"], "execution_receipt.v1.json")
        self.assertIn("first_divergence", schema["properties"])
        self.assertIn("remedy", schema["properties"])
        self.assertIn("verification", schema["properties"])
        self.assertNotIn("dispatch", schema["required"])
        self.assertNotIn("receipts", schema["required"])
        self.assertNotIn("dispatch", schema["properties"])
        self.assertNotIn("receipts", schema["properties"])

    def test_valid_clean_record(self):
        self.assertEqual(validator.validate_record(make_record()), [])

    def test_soft_failure_uses_semantic_status_not_exit_code(self):
        record = make_record(status="failed", disposition="revise", divergence={
            "owner": "implementation",
            "stage": "execution_gate",
            "criterion": "R1",
            "evidence_refs": ["ground-truth.json"],
            "reason_codes": ["criterion_failed"],
        }, remedy={
            "consumer": {"kind": "evaluation", "target": "fixture"},
            "action": "apply the correction and rerun the gate",
            "evidence_refs": ["ground-truth.json"],
            "status": "pending",
            "verification_check_ids": ["R1"],
        })
        record["receipt"]["exit_code"] = 0
        record["receipt"]["reason_codes"] = ["soft_semantic_failure"]
        record["receipt_id"] = validator._receipt_id(record["receipt"])
        record["verification"]["receipt_ids"] = [record["receipt_id"]]
        record["evidence_id"] = hashlib.sha256(
            validator._canonical({key: value for key, value in record.items() if key != "evidence_id"})
        ).hexdigest()
        self.assertEqual(validator.validate_record(record), [])

    def test_clean_record_may_omit_conditional_fields(self):
        record = make_record()
        for key in ("correction", "first_divergence", "remedy"):
            record.pop(key)
        record["evidence_id"] = hashlib.sha256(
            validator._canonical({key: value for key, value in record.items() if key != "evidence_id"})
        ).hexdigest()
        self.assertEqual(validator.validate_record(record), [])

    def test_rejects_legacy_receipt_collection(self):
        record = make_record()
        record["receipts"] = []
        record["evidence_id"] = hashlib.sha256(
            validator._canonical({key: value for key, value in record.items() if key != "evidence_id"})
        ).hexdigest()
        errors = validator.validate_record(record)
        self.assertTrue(any("unexpected property 'receipts'" in error for error in errors))

    def test_denied_and_timed_out_receipts_map_to_failed(self):
        for status in ("denied", "timed_out"):
            with self.subTest(status=status):
                record = make_record(status=status, disposition="revise", divergence={
                    "owner": "execution", "stage": "execution_gate", "criterion": "R1",
                    "evidence_refs": ["ground-truth.json"], "reason_codes": [status],
                }, remedy={
                    "consumer": {"kind": "evaluation", "target": "fixture"},
                    "action": "rerun the gate", "evidence_refs": ["ground-truth.json"],
                    "status": "pending", "verification_check_ids": ["R1"],
                })
                self.assertEqual(validator.validate_record(record), [])

    def test_rejects_unsafe_artifact_references(self):
        record = make_record()
        record["receipt"]["artifact_hashes"] = {"../outside": "a" * 64}
        record["output"]["artifact_refs"] = ["../outside"]
        record["output"]["artifact_hashes"] = {"../outside": "a" * 64}
        record["output"]["panel_ref"] = "../outside"
        record["evidence_id"] = hashlib.sha256(
            validator._canonical({key: value for key, value in record.items() if key != "evidence_id"})
        ).hexdigest()
        errors = validator.validate_record(record)
        self.assertTrue(any("unsafe" in error for error in errors))

    def test_rejects_null_check_and_invalid_output_shape(self):
        record = make_record()
        record["checks"] = [None]
        record["evidence_id"] = hashlib.sha256(
            validator._canonical({key: value for key, value in record.items() if key != "evidence_id"})
        ).hexdigest()
        errors = validator.validate_record(record)
        self.assertTrue(any("checks[0]" in error for error in errors))

        record = make_record()
        record["output"] = None
        record["evidence_id"] = hashlib.sha256(
            validator._canonical({key: value for key, value in record.items() if key != "evidence_id"})
        ).hexdigest()
        errors = validator.validate_record(record)
        self.assertTrue(any("expected ['object']" in error or "expected" in error for error in errors))

    def test_rejects_extra_field_inside_strict_receipt(self):
        record = make_record()
        record["receipt"]["receipt_id"] = "not-permitted"
        errors = validator.validate_record(record)
        self.assertTrue(any("unexpected property 'receipt_id'" in error for error in errors))

    def test_rejects_empty_receipt_artifacts(self):
        record = make_record()
        record["receipt"]["artifact_hashes"] = {}
        record["receipt_id"] = validator._receipt_id(record["receipt"])
        record["verification"]["receipt_ids"] = [record["receipt_id"]]
        record["evidence_id"] = hashlib.sha256(
            validator._canonical({key: value for key, value in record.items() if key != "evidence_id"})
        ).hexdigest()
        errors = validator.validate_record(record)
        self.assertIn("receipt.artifact_hashes must retain at least one artifact hash", errors)

    def test_verified_remedy_requires_parent_lineage(self):
        record = make_record(status="passed", divergence={
            "owner": "implementation",
            "stage": "execution_gate",
            "criterion": "R1",
            "evidence_refs": ["ground-truth.json"],
            "reason_codes": ["criterion_failed"],
        }, remedy={
            "consumer": {"kind": "evaluation", "target": "fixture"},
            "action": "rerun the corrected implementation",
            "evidence_refs": ["ground-truth.json"],
            "status": "verified",
            "verification_check_ids": ["R1"],
        }, disposition="promote")
        record["verification"]["status"] = "passed"
        record["evidence_id"] = hashlib.sha256(
            validator._canonical({key: value for key, value in record.items() if key != "evidence_id"})
        ).hexdigest()
        errors = validator.validate_record(record)
        self.assertIn("verified remedy requires parent evidence lineage", errors)


if __name__ == "__main__":
    unittest.main()
