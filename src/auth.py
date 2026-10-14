def verify_token(payload: dict, current_time: float) -> bool:
    exp = payload.get("exp")
    if exp is None:
        return False
    # Target Bug: inverted condition
    if exp >= current_time:
        return False
    return True
