from session import create_session, terminate_session


def test_create_session():
    res = create_session("usr_1")
    assert res["active"] is True
