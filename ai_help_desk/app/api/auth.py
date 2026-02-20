from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.database import get_connection
from app.repositories.session_repository import SessionRepository
import uuid

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(request: LoginRequest):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT user_id, role
        FROM users
        WHERE username = %s AND password = %s
        """,
        (request.username, request.password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    user_id, role = user

    session_id = str(uuid.uuid4())

    session_repo = SessionRepository()

    session_repo.save_message(
        session_id=session_id,
        user_id=user_id,
        role=role,
        message="SESSION_STARTED"
    )

    return {
        "message": "Login successful",
        "sessionId": session_id,
        "userId": str(user_id),
        "role": role
    }
