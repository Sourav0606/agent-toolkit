from validator import validate_order


def test_vip_high_order():
    # VIP order of 5,000 should be allowed (under 10,000 limit)
    res = validate_order("usr_99", amount=5000.0, is_vip=True)
    assert res == {"status": "ok", "code": 200}


def test_regular_high_order():
    # Regular order of 5,000 should be rejected (over 1,000 limit)
    res = validate_order("usr_99", amount=5000.0, is_vip=False)
    assert res == {"status": "error", "code": 400}
