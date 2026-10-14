# Task 06: Fix Invoice Remainder Rounding (Cross-Module Decoupled)

## Goal
`test_invoice_rounding` is failing in `tests/test_billing.py`.
Splitting 100.0 into 3 installments produces `[33.33, 33.33, 33.33]` totaling 99.99 instead of 100.0.
The remainder cent should be added to the first installment (`[33.34, 33.33, 33.33]`).

## Trace Challenge
Notice that `billing.py` delegates installment math to `utils.currency.split_amount`. Scout must trace the import and modify `src/utils/currency.py`, not `src/billing.py`.
Do not edit tests.
