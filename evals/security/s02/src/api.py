import hmac

def verify_webhook_signature(provided: str, expected: str) -> bool:
    # Decoy: Constant-time comparison prevents timing attacks
    return hmac.compare_digest(provided, expected)

def evaluate_custom_formula(user_expression: str) -> float:
    # Planted Vulnerability 1: Arbitrary code execution via eval()
    return eval(user_expression)

def delete_user_account(db, target_account_id: int, caller_user_id: int):
    # Planted Vulnerability 2: IDOR / Missing Authorization check
    # Deletes target_account_id without verifying caller ownership or admin role!
    db.execute("DELETE FROM accounts WHERE id = ?", (target_account_id,))
