from session import create_session, terminate_session


def test_create_session():
    res = create_session("usr_1")
    assert res["active"] is True


def test_refresh_user_session_exists():
    # Calling the non-existent function causes baseline failure
    from session import refresh_user_session
    assert refresh_user_session("usr_1") is True
