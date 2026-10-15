from users import get_user_profile

def test_get_user_profile():
    res = get_user_profile("u1")
    assert res == {"id": "u1", "name": "User_u1"}
