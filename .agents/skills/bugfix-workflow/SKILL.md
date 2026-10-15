---
name: bugfix-workflow
description: Use when asked to fix a bug or make a small code change in this repo. Runs scout, fixer, tests and auditor in a bounded loop.
---

# Bounded Bug-Fix Workflow

Follow these steps in strict order:

0. **Read Guidelines**: Read `AGENTS.md`. Use its test commands and obey its limits.
1. **Baseline Test**: Run the full test command from `AGENTS.md` (`python3 -m pytest -q --tb=short`) once before editing using `run_command`. Note which tests already fail.
2. **Scout Phase**: Delegate to the `scout` subagent with the task description. If status is `not_found`, ask the user for clarification. Do not guess or proceed blindly.
3. **Fix Phase**: Delegate to the `fixer` subagent with:
   - The task description
   - Scout's symbol context and related signatures
   - Any notes from previous failed attempts
4. **Deterministic Verification**: Run the tests yourself with `run_command` using the commands in `AGENTS.md`.
   - Trust the process exit code and output, never an agent's claim.
   - Done means: tests related to the task pass, and no test that passed before now fails.
   - If tests pass: Inspect the diff. Verify no test files were modified, no assertions removed, and no skip markers added. Then report the passing diff to the user.
5. **Auditor Loop on Failure**: If tests fail:
   - Delegate to the `test-auditor` subagent with the exit code, failing test names, minimal traceback, and baseline comparison.
   - If verdict is `impl_bug`: Return to Step 3 (Fix Phase), passing the auditor's 5-line failure summary.
   - If verdict is `test_bug`, `env_issue`, or `ambiguous_spec`: Stop and report to the user immediately.

## Escalation and Safety:

Follow the Failure Escalation Rules in `AGENTS.md`.
Finish with: the final git diff, the passing test output, and any areas not verified.
