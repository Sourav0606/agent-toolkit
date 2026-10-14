import pytest
from auth import verify_token


def test_verify_token_valid():
    # Token expires in the future (1000 > 800) -> should be valid (True)
    payload = {"sub": "user_123", "exp": 1000}
    assert verify_token(payload, current_time=800) is True


def test_verify_token_expired():
    # Token expired in the past (500 < 800) -> should be invalid (False)
    payload = {"sub": "user_123", "exp": 500}
    assert verify_token(payload, current_time=800) is False


def test_verify_token_missing_exp():
    # Token missing exp claim -> should be invalid (False)
    payload = {"sub": "user_123"}
    assert verify_token(payload, current_time=800) is False
