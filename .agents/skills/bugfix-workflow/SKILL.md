---
name: bugfix-workflow
description: Use when asked to fix a bug or make a small code change in this repo. Runs scout, fixer, tests and auditor in a bounded loop.
---

# Bounded Bug-Fix Workflow

Follow these steps in strict order:

1. **Baseline Test**: Run the test command from `AGENTS.md` once before editing using `run_command`. Note which tests already fail.
2. **Scout Phase**: Delegate to the `scout` subagent with the task description. If status is `not_found`, ask the user for clarification. Do not guess or proceed blindly.
3. **Fix Phase**: Delegate to the `fixer` subagent with:
   - The task description
   - Scout's symbol context and related signatures
   - Any notes from previous failed attempts
4. **Deterministic Verification**: Run the tests yourself with `run_command`.
   - Trust the process exit code, never an agent's claim.
   - If tests pass (exit code 0): Inspect the diff. Verify no test files were modified, no assertions removed, and no skip markers added. Then report the passing diff to the user.
5. **Auditor Loop on Failure**: If tests fail (non-zero exit code):
   - Delegate to the `test-auditor` subagent with the exit code, failing test names, minimal traceback, and baseline comparison.
   - If verdict is `impl_bug`: Return to Step 3 (Fix Phase), passing the auditor's 5-line failure summary.
   - If verdict is `test_bug`, `env_issue`, or `ambiguous_spec`: Stop and report to the user immediately.

## Safety and Loop Limits:
- **Maximum 3 fix attempts**.
- **Stagnation detection**: If the same test fails with the identical error twice in a row, stop and report rather than repeating the attempt.
- Finish with: the final git diff, the passing test output, and any areas not verified.
