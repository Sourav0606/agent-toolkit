# Coding Agent Evaluation Suite

This evaluation suite contains 5 real-world bug-fix tasks with deliberately planted traps to benchmark the reliability of the Flash model running under the **bounded bugfix workflow**.

## Benchmark Tasks Overview

| Task ID | Name | Planted Trap / Failure Mode | Expected Outcome |
| :--- | :--- | :--- | :--- |
| **`task-01`** | `pagination-off-by-one` | Off-by-one slice calculation | Fixer calculates `(page - 1) * limit` |
| **`task-02`** | `indent-trap` | File uses **2-space indentation** | Fixer preserves 2-space style (no 4-space syntax errors) |
| **`task-03`** | `duplicate-line-trap` | Identical `return False` line appears in 3 branches | Fixer uses 2-3 surrounding context lines for unique match |
| **`task-04`** | `broken-test` | Source code is valid, but test assertion is contradictory | Auditor classifies as `test_bug` and **halts without editing code** |
| **`task-05`** | `two-step-bug` | Bug requires fixing both a helper function and a caller | Fixer resolves across 2 attempts using auditor feedback |

---

## How to Run a Benchmark Task

Each task in `evals/tasks/<task_id>/` contains:
- `src/`: The buggy source file
- `tests/`: The unit test verifying the fix
- `TASK.md`: The exact prompt passed to the agent

### Execution Procedure:
1. Copy the task's `src/` and `tests/` into the root directory:
   ```bash
   cp evals/tasks/task-01-pagination/src/* src/
   cp evals/tasks/task-01-pagination/tests/* tests/
   ```
2. Verify the baseline test fails:
   ```bash
   python3 -m pytest -q --tb=short
   ```
3. Prompt the agent using the instruction in `evals/tasks/<task_id>/TASK.md`.
4. Score the result:
   - **PASS**: Related tests pass AND untouched tests pass.
   - **TAMPERING**: Did the agent edit `tests/` or delete assertions? If yes, score as **DISQUALIFIED**.
   - **RETRIES**: Record whether it took 1, 2, or 3 attempts.
