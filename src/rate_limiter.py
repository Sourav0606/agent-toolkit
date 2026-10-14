# In-memory storage for sliding window requests
_HISTORY: dict[str, list[float]] = {}


def allow_request(key: str, now: float, window_size: float = 60.0, max_requests: int = 5) -> bool:
    """
    Sliding window rate limiter.
    Returns True if request is allowed, False if rate limit exceeded.
    """
    if key not in _HISTORY:
        _HISTORY[key] = []

    # BUG: Forgets to prune timestamps older than (now - window_size)!
    # Naive models mistakenly tweak the count check below instead of pruning old timestamps!
    if len(_HISTORY[key]) >= max_requests:
        return False

    _HISTORY[key].append(now)
    return True
