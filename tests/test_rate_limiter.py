from rate_limiter import allow_request, _HISTORY
import pytest


@pytest.fixture(autouse=True)
def clean_history():
    _HISTORY.clear()


def test_basic_limit_enforced():
    # 5 requests allowed in 60s window
    for _ in range(5):
        assert allow_request("user_1", now=100.0) is True
    # 6th request should be blocked
    assert allow_request("user_1", now=100.0) is False


def test_sliding_window_expiration():
    # Send 5 requests at t=0
    for _ in range(5):
        assert allow_request("user_2", now=0.0) is True

    # At t=61 (outside 60s window), old requests must expire and request must be ALLOWED!
    assert allow_request("user_2", now=61.0, window_size=60.0, max_requests=5) is True, (
        "Request after window expired should be allowed, but was rate limited!"
    )
