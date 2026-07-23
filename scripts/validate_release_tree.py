#!/usr/bin/env python3
"""Fail closed on private operational material in the public export tree."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".py", ".toml", ".yaml", ".yml", ".txt"}
RULES = {
    "concrete_home": re.compile(r"/(?:Users|home)/(?!<user>/|runner/)[A-Za-z0-9._-]+/"),
    "private_tree": re.compile(r"(?:^|[ /`])(?:handovers|reviews|\.state|runs|deprecated|data/candidates)/"),
    "private_host_or_volume": re.compile(r"\b(?:spark-[A-Za-z0-9-]+|linux-backend|WD_BUp)\b", re.I),
    "private_role_alias": re.compile(r"\bProduct [AB]\b|\bproduct_[ab]\b"),
    "session_language": re.compile(r"\b(?:starter prompt|resume this session|handover to)\b", re.I),
}


def main() -> int:
    findings = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.suffix not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(ROOT)
        # This file necessarily contains the patterns it enforces. Its behaviour
        # is covered by tests; scanning its regex declarations reports false
        # positives rather than release-tree leaks.
        if relative == Path("scripts/validate_release_tree.py"):
            continue
        for number, line in enumerate(path.read_text(errors="replace").splitlines(), 1):
            for rule, pattern in RULES.items():
                if pattern.search(line):
                    findings.append(f"{relative}:{number}:{rule}")
    if findings:
        print("\n".join(findings))
        return 1
    print("PASS public release tree")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
