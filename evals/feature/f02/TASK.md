# Task f02: Currency parameter extension

## Goal
Extend `format_currency(amount: float)` in `src/money.py` to accept an optional `symbol: str = "$"` parameter.

Requirements:
- If `symbol` is not provided, it defaults to "$".
- If `symbol` is provided (e.g. "€" or "£"), it formats with that symbol (e.g. `format_currency(10.5, symbol="€") -> "€10.50"`).

Follow feature-workflow: write a test first in a new test file, then implement. Do NOT edit existing test files.
