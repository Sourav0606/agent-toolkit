# Task 09: Fix Sliding Window Rate Limiter (Obvious Fix Trap)

## Goal
In `src/rate_limiter.py`, `test_sliding_window_expiration` is failing.
Requests sent after the 60s window has expired are incorrectly rejected.

## Trap
Do not simply increase `max_requests` or alter the `>=` comparison.
The root cause is that timestamps older than `now - window_size` are not pruned from the request history. Prune expired entries so new requests within the window are correctly permitted.
Do not edit tests.
