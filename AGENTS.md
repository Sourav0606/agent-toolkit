# Project Agent Guidelines (AGENTS.md)

This file defines the project conventions, verification commands, and security boundaries for all agents working in this repository.

## Verification & Test Command
- **Test Command**: `python3 -m pytest`
- Tests must be executed deterministically. Exit code 0 is required for task completion.

## Code & Formatting Conventions
- **Language**: Python 3.12+
- **Indentation**: 4 spaces, no tabs.
- **Type Annotations**: Use Python standard type hints.
- **Edits**: Minimal, surgical changes only. Do not reformat untouched lines.

## Protected Paths (DO NOT MODIFY)
The following files and paths are strictly protected and must never be edited during automated fixes without explicit user permission:
- `.env*`
- `.github/` and `.gitlab/` CI configurations
- Dependency lockfiles (`poetry.lock`, `package-lock.json`, etc.)
- Test files (`test_*.py`, `*_test.py`, `tests/`) are READ-ONLY for implementation fixers to prevent test tampering.

## Failure Escalation Rules
- Maximum 3 fix attempts per task.
- If the same test fails with the identical signature consecutively, the agent must halt and request human clarification.
