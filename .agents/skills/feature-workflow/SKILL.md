---
name: feature-workflow
description: Use when implementing a new feature, adding an endpoint, or extending functionality. Works test-first, never modifies existing tests, and respects Ponytail minimal-code discipline.
---

# Feature Implementation Workflow

A test-first, bounded workflow for safely adding new functionality.

## Step 0: Check Requirements
1. Read the feature request. If requirements are ambiguous, missing acceptance criteria, or lack parameters, **STOP immediately** and ask the user for clarification. Do not guess.

## Step 1: Explore Call Graph (Scout)
2. Call `invoke_subagent scout` to locate where this feature plugs into the codebase:
   - Identify existing modules, sibling functions, and shared utilities.
   - Run baseline test suite (`python3 -m pytest -q --tb=short`). All existing tests must pass before proceeding.

## Step 2: Contradiction Check
3. Verify that the requested feature does not contradict existing tests or API contracts. If an existing test would break under the requested design, **STOP** and alert the user. Never modify existing tests to accommodate new features.

## Step 3: Write Test First (Test-Writer)
4. Call `invoke_subagent test-writer` to create exactly ONE new test file under `tests/` (e.g. `tests/test_<feature>.py`).
5. Run the new test suite (`python3 -m pytest -q --tb=short tests/test_<feature>.py`).
   - The new test MUST fail with an `ImportError`, `AttributeError`, or `AssertionError` against untouched code.

## Step 4: Implement Minimum Code (Fixer)
6. Call `invoke_subagent fixer` to write the implementation in `src/`.
   - **Ponytail Rule**: Write the minimum code needed to pass the new test. Reuse existing helpers and Python standard library features. Do not introduce new abstractions or unrequested options.

## Step 5: Verification & Regression Loop
7. Run the full test suite (`python3 -m pytest -q --tb=short`).
   - Done when: The new test passes AND all pre-existing tests continue to pass.
   - If tests fail, feed output back to `fixer` (up to a 3-attempt cap).
   - If `tests/` diff shows any edits to pre-existing test files, immediately revert those edits.
