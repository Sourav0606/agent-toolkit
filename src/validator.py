def validate_order(user_id: str, amount: float, is_vip: bool) -> dict:
    """
    Validate order checkout criteria.
    """
    if not user_id:
        # Branch 1
        return {"status": "error", "code": 400}

    if amount <= 0:
        # Branch 2
        return {"status": "error", "code": 400}

    # VIP maximum limit is 10,000; Regular maximum limit is 1,000
    # BUG in Branch 3: Hardcoded limit of 100 for VIPs instead of 10,000!
    if is_vip and amount > 100:
        return {"status": "error", "code": 400}

    if not is_vip and amount > 1000:
        # Branch 4
        return {"status": "error", "code": 400}

    return {"status": "ok", "code": 200}
