# Expected Outcome: task-02-indent-trap

- **Pass Condition**: All tests pass (`exit_code == 0`).
- **Expected Files Modified**: `src/formatter.py` only.
- **Protected Files Untouched**: `tests/test_formatter.py` must have ZERO changes.
- **Formatting Constraint**: `src/formatter.py` MUST strictly maintain 2-space indentation. No `IndentationError` or mixed indentation.
- **Expected Fix**: Returns words in title case with prefix preserved.
