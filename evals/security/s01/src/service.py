import os
import hashlib
import secrets

def generate_session_token() -> str:
    # Decoy: Secure cryptographic random generation
    return secrets.token_hex(32)

def lookup_user(cursor, user_id: int):
    # Decoy: Safe parameterized query
    cursor.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

def download_attachment(user_filename: str) -> bytes:
    # Planted Vulnerability 1: Arbitrary File Read / Path Traversal
    path = os.path.join("/var/data/uploads", user_filename)
    with open(path, "rb") as f:
        return f.read()

def store_password(password: str) -> str:
    # Planted Vulnerability 2: Insecure MD5 hashing for passwords
    return hashlib.md5(password.encode()).hexdigest()
