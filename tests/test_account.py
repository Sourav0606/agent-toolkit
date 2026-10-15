from account import validate_password


def test_valid_strong_password():
    assert validate_password("SecurePass123!") is True


def test_missing_special_character():
    # Must fail on current code because special char is missing
    assert validate_password("NoSpecialChar123") is False


def test_too_short_password():
    assert validate_password("Short1!") is False
