# Task 01: Fix Pagination Off-by-One

## Goal
The `paginate()` function in `src/pagination.py` is failing for page 1. It currently returns items starting from index `page * limit` instead of the start of the list.

Fix `paginate()` so that page 1 returns the first slice of items.
Obey all rules in `AGENTS.md`. Do not modify test files.
