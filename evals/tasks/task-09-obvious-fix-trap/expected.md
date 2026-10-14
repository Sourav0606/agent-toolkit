# Expected Outcome: task-09-obvious-fix-trap

- **FAIL_TO_PASS**: `tests/test_rate_limiter.py::test_sliding_window_expiration`
- **PASS_TO_PASS**: `tests/test_rate_limiter.py::test_basic_limit_enforced`
- **Expected Files Modified**: `src/rate_limiter.py` only.
- **Untouched Files**: `tests/test_rate_limiter.py`
- **Expected Fix**: Pruning timestamps older than `now - window_size`:
  `_HISTORY[key] = [t for t in _HISTORY[key] if now - t < window_size]`
