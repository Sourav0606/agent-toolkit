# Task 05: Fix Checkout Calculation (Two-Step Bug)

## Goal
In `src/checkout.py`, the checkout calculation is failing.
Both `test_compute_discount` and `test_checkout_total_with_discount` are failing.

## Structure
- `compute_discount` has a percentage calculation bug.
- `checkout_total` fails to subtract the computed discount from subtotal.
Fix both issues so that all checkout tests pass.
Do not edit tests.
