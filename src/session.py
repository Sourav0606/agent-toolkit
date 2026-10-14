def create_session(user_id: str) -> dict:
    return {"user_id": user_id, "active": True}


def terminate_session(session_id: str) -> bool:
    return True
