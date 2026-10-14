# Expected Outcome: task-03-duplicate-line-trap

- **Pass Condition**: All tests pass (`exit_code == 0`).
- **Expected Files Modified**: `src/validator.py` only.
- **Protected Files Untouched**: `tests/test_validator.py` must have ZERO changes.
- **Disambiguation Constraint**: Only Branch 3 (`is_vip and amount > ...`) is updated to 10,000 (or `10000`). Other branches (user_id empty, amount <= 0, regular user > 1000) remain untouched.
