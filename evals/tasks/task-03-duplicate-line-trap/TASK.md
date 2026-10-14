# Task 03: VIP Limit (Duplicate Lines Trap)

## Goal
In `src/validator.py`, VIP orders should be permitted up to 10,000. Currently, `is_vip and amount > 100` incorrectly rejects valid VIP orders over 100.

## Trap
The line `return {"status": "error", "code": 400}` appears in 4 different `if` blocks across this function.
Your Search & Replace block MUST include the surrounding condition lines (`if is_vip and ...`) to avoid duplicate match ambiguity errors.
Do not edit tests.
