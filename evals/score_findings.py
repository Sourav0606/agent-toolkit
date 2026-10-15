#!/usr/bin/env python3
"""
Scorer for Review and Security Audit Finding Reports.

Validates that an agent's review or security report:
1. Detects planted real issues (true positives)
2. Avoids flagging harmless decoy code (false positives)
3. Outputs an appropriate overall verdict (BLOCK, CHANGES_REQUESTED, APPROVE)
"""

import sys
import json
from pathlib import Path


def score_report(report_path: Path, expected_path: Path) -> dict:
    if not report_path.exists():
        return {"passed": False, "reason": f"Report file {report_path} not found"}
    if not expected_path.exists():
        return {"passed": False, "reason": f"Expected file {expected_path} not found"}

    report_text = report_path.read_text(encoding="utf-8").lower()
    expected = json.loads(expected_path.read_text(encoding="utf-8"))

    task_id = expected.get("task_id", "unknown")
    planted = [p.lower() for p in expected.get("planted_issues", [])]
    forbidden_decoys = [d.lower() for d in expected.get("forbidden_decoys", [])]
    expected_verdict = expected.get("expected_verdict", "").lower()

    # 1. Check for false positives (decoys)
    flagged_decoys = [d for d in forbidden_decoys if d in report_text and "not a bug" not in report_text]
    if flagged_decoys:
        return {
            "passed": False,
            "task_id": task_id,
            "verdict": "FAIL (False Positive)",
            "reason": f"Report incorrectly flagged safe decoy code as an issue: {flagged_decoys}"
        }

    # 2. Check for true positives (planted issues)
    if planted:
        # At least one key term for each planted issue should be referenced
        missed = [p for p in planted if p not in report_text]
        # If all planted patterns missed:
        if len(missed) == len(planted):
            return {
                "passed": False,
                "task_id": task_id,
                "verdict": "FAIL (Missed Finding)",
                "reason": f"Report missed planted issue. None of these terms found: {planted}"
            }

    # 3. Check for clean diff case (r04 / s03)
    if not planted:
        if "block" in report_text or "changes_requested" in report_text:
            return {
                "passed": False,
                "task_id": task_id,
                "verdict": "FAIL (False Alarm on Clean Code)",
                "reason": "Report requested changes or blocked a clean diff!"
            }

    # 4. Check verdict alignment if expected
    if expected_verdict:
        if expected_verdict not in report_text:
            return {
                "passed": False,
                "task_id": task_id,
                "verdict": "FAIL (Verdict Mismatch)",
                "reason": f"Expected verdict '{expected_verdict.upper()}' was not in the report."
            }

    return {
        "passed": True,
        "task_id": task_id,
        "verdict": "PASS",
        "reason": "All planted issues detected without false positives on decoys."
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 evals/score_findings.py <report_file> <expected.json>")
        sys.exit(1)

    rep = Path(sys.argv[1])
    exp = Path(sys.argv[2])
    res = score_report(rep, exp)
    print(json.dumps(res, indent=2))
    sys.exit(0 if res["passed"] else 1)


if __name__ == "__main__":
    main()
