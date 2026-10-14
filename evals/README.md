# Coding Agent Evaluation Suite

This evaluation suite contains 5 real-world bug-fix tasks with deliberately planted traps to benchmark the reliability of the Flash model running under the **bounded bugfix workflow**.

## Benchmark Tasks Overview

| Task ID | Name | Planted Trap / Failure Mode | Expected Outcome (`expected.md`) |
| :--- | :--- | :--- | :--- |
| **`task-01`** | `pagination-off-by-one` | Off-by-one slice calculation | Fixer calculates `(page - 1) * limit`. All tests pass. |
| **`task-02`** | `indent-trap` | File uses **2-space indentation** | Fixer preserves 2-space style (no 4-space syntax errors). All tests pass. |
| **`task-03`** | `duplicate-line-trap` | Identical `return {"status": "error", "code": 400}` appears in 4 branches | Fixer uses 2-3 surrounding context lines for unique match on VIP branch. All tests pass. |
| **`task-04`** | `broken-test` | Source code is valid, but test assertion is contradictory | Auditor classifies as `test_bug`. **Agent halts without editing code (`src/` and `tests/` untouched).** |
| **`task-05`** | `two-step-bug` | Bug requires fixing both a helper function and a caller | Fixer resolves both issues (1 or 2 attempts recorded as data). All tests pass. |

---

## Automated Reset and Scoring Script (`evals/score_task.py`)

Instead of manual file copying and error-prone checks, use `evals/score_task.py`:

### 1. Reset a Task (Cleans stale files, copies files, verifies baseline failure):
```bash
python3 evals/score_task.py reset task-01-pagination
```

### 2. Run the Workflow:
Prompt the agent with the task goal from `evals/tasks/<task_id>/TASK.md`.

### 3. Automatically Score the Result:
```bash
python3 evals/score_task.py score task-01-pagination
```
Checks:
- Process exit code from `python3 -m pytest -q --tb=short`.
- **Anti-Tampering**: Asserts `tests/` is completely untouched.
- **Scope Guard**: Asserts only the designated `src/` file was modified.
- **Task Specifics**: Indentation style (2 spaces for task-02), zero files touched (for task-04).
