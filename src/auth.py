def verify_token(payload: dict, current_time: float) -> bool:
    """
    Verify JWT payload expiration.
    Returns True if token is valid, False if expired or missing exp.
    """
    exp = payload.get("exp")
    if exp is None:
        return False

    # Reject token if expired (expiration time is before or equal to current time)
    if exp <= current_time:
        return False

    return True
