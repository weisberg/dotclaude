#!/usr/bin/env python3
"""Run ultracode-high gates from a JSON manifest.

Exit codes:
  0  all gates passed
  1  at least one gate genuinely failed (the work did not meet a gate)
  2  the manifest or a gate is malformed (a configuration/runner problem, not a
     real failure) — fail closed so a typo can never read as a clean pass
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def result(gate, status, evidence):
    return {
        "id": gate.get("id"),
        "type": gate.get("type"),
        "description": gate.get("description"),
        "status": status,
        "evidence": evidence,
    }


def run_gate(gate):
    gate_type = gate.get("type")

    try:
        if gate_type == "command":
            cmd = gate.get("cmd")
            if not cmd:
                return result(gate, "error", {"reason": "command gate missing 'cmd'"})
            completed = subprocess.run(
                cmd,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            evidence = {
                "cmd": cmd,
                "returncode": completed.returncode,
                "stdout_tail": completed.stdout[-1000:],
                "stderr_tail": completed.stderr[-1000:],
            }
            return result(gate, "passed" if completed.returncode == 0 else "failed", evidence)

        if gate_type == "file_exists":
            raw_path = gate.get("path")
            if not raw_path:
                return result(gate, "error", {"reason": "file_exists gate missing 'path'"})
            path = Path(raw_path)
            return result(gate, "passed" if path.exists() else "failed", {"path": str(path)})

        if gate_type == "grep":
            raw_path = gate.get("path")
            pattern = gate.get("pattern")
            if not raw_path or pattern is None:
                return result(gate, "error", {"reason": "grep gate requires 'path' and 'pattern'"})
            path = Path(raw_path)
            if not path.exists():
                return result(gate, "failed", {"path": str(path), "reason": "missing"})
            text = path.read_text(encoding="utf-8", errors="replace")
            try:
                matched = re.search(pattern, text, flags=re.MULTILINE) is not None
            except re.error as exc:
                return result(gate, "error", {"path": str(path), "pattern": pattern, "reason": f"invalid regex: {exc}"})
            # `negate: true` asserts the pattern must NOT appear.
            negate = bool(gate.get("negate", False))
            ok = (not matched) if negate else matched
            return result(
                gate,
                "passed" if ok else "failed",
                {"path": str(path), "pattern": pattern, "negate": negate, "matched": matched},
            )

        if gate_type == "attest":
            if "answer" not in gate:
                return result(gate, "error", {"reason": "attest gate missing boolean 'answer'"})
            passed = gate.get("answer") is True
            status = "passed" if passed else "failed"
            return result(gate, status, {"attest_flagged": True, "evidence": gate.get("evidence")})

        return result(gate, "error", {"reason": f"unknown gate type {gate_type!r}"})

    except Exception as exc:  # never let one malformed gate crash the whole run
        return result(gate, "error", {"reason": f"gate raised {type(exc).__name__}: {exc}"})


def main():
    parser = argparse.ArgumentParser(description="Run ultracode-high gates from a JSON manifest.")
    parser.add_argument("manifest", help="JSON file containing {'gates': [...]}")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    try:
        raw = manifest_path.read_text(encoding="utf-8")
    except OSError as exc:
        print(json.dumps({"error": f"cannot read manifest: {exc}"}, indent=2))
        return 2
    try:
        manifest = json.loads(raw)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"manifest is not valid JSON: {exc}"}, indent=2))
        return 2

    gates = manifest.get("gates") if isinstance(manifest, dict) else None
    if not isinstance(gates, list):
        print(json.dumps({"error": "manifest must contain a gates list"}, indent=2))
        return 2

    results = [run_gate(gate) for gate in gates]
    errored = any(item["status"] == "error" for item in results)
    failed = any(item["status"] == "failed" for item in results)
    passed = all(item["status"] == "passed" for item in results)
    print(json.dumps({"passed": passed, "results": results}, indent=2))
    if errored:
        return 2
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
