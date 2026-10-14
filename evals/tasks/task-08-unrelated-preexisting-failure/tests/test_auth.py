from auth import verify_token


def test_verify_token():
    assert verify_token({"exp": 1000}, current_time=800) is True
    assert verify_token({"exp": 500}, current_time=800) is False
