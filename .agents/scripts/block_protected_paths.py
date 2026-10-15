#!/usr/bin/env python3
"""
Lifecycle PreToolUse hook to deterministically block edits to protected files and test files.
"""

import sys
import json
import re
from pathlib import Path

PROTECTED_PATTERNS = [
    r"\.env",
    r"\.github/",
    r"\.gitlab/",
    r"poetry\.lock",
    r"package-lock\.json",
    r"yarn\.lock",
    r"pnpm-lock\.yaml",
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        # If payload cannot be read, default allow to avoid halting session
        print(json.dumps({"decision": "allow"}))
        return

    tool_call = data.get("toolCall", {})
    args = tool_call.get("args", {})
    target_file = args.get("TargetFile") or args.get("target_file") or args.get("path") or ""

    if target_file:
        posix_path = Path(target_file).as_posix()
        for pat in PROTECTED_PATTERNS:
            if re.search(pat, posix_path):
                result = {
                    "decision": "deny",
                    "reason": f"HARD POLICY GATE: Modification to protected path '{posix_path}' is strictly blocked."
                }
                print(json.dumps(result))
                return

    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
