import re


def validate_password(password: str) -> bool:
    """
    Validate password complexity:
    1. At least 8 characters
    2. At least one digit (0-9)
    3. At least one special character (!@#$%^&*()_+-=)
    """
    if len(password) < 8:
        return False

    if not re.search(r"\d", password):
        return False

    if not re.search(r"[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]", password):
        return False

    return True
