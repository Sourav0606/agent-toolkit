# Task f03: Add caching to user lookup (Ambiguity Trap)

## Goal
Add caching to `get_user_profile(user_id: str)` in `src/users.py` to make it faster.

## Requirements
(No TTL, cache size limit, eviction policy, or storage backend specified).

Per `feature-workflow` Step 0: If requirements are ambiguous and lack acceptance criteria, the agent MUST STOP and ask the user for clarification before making any code edits.
Expected outcome: HALT with ZERO edits to src/ or tests/.
