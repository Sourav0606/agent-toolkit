# Project Agent Guidelines

## Layout
- Source: `src/`  |  Tests: `tests/`
- Dependencies are already installed. Do not install packages or use the network.

## Verification
- Full run: `python3 -m pytest -q --tb=short`
- Single test: `python3 -m pytest -q --tb=short <path>::<test_name>`
- Always run the full suite once BEFORE editing and record which tests already fail.
- Done means: tests related to the task pass, and no test that passed before now fails.
- Trust the command's exit code and output, not any agent's claim.

## Conventions
- Python 3.12+, 4-space indentation, no tabs, standard type hints.
- Minimal, surgical edits. Do not reformat or touch unrelated lines.

## Protected Paths (never edit without explicit user permission)
- `.env*`, `.github/`, `.gitlab/`, lockfiles (`poetry.lock`, `package-lock.json`, ...)
- Test files (`test_*.py`, `*_test.py`, `tests/`) are read-only during bug fixes.
  If the fix seems to need a test change, stop and ask the user.
- Never weaken tests: no removed assertions, no added skip/xfail.

## Failure Escalation
- Maximum 3 fix attempts per task.
- If the same test fails with the same error twice in a row, stop and report.
- If context is missing, report what is missing. Do not guess.
