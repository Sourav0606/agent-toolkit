# Expected Outcome: task-05-two-step-bug

- **Pass Condition**: All tests pass (`exit_code == 0`).
- **Expected Files Modified**: `src/checkout.py` only.
- **Protected Files Untouched**: `tests/test_checkout.py` must have ZERO changes.
- **Expected Fixes**:
  1. `compute_discount`: divides by `100.0` instead of `10.0`.
  2. `checkout_total`: subtracts `discount` from `subtotal` before returning.
- **Attempts Data**: May resolve in 1 attempt (if fixer tackles both functions simultaneously) or 2 attempts (fixing one function per attempt using auditor feedback). Both are valid passes.
