import hmac
import secrets

def secure_token_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a, b)

def query_user_safely(cursor, username: str):
    cursor.execute("SELECT id, email FROM users WHERE username = ?", (username,))
    return cursor.fetchone()
