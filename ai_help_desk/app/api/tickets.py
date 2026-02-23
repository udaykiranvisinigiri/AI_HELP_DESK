from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.services.ticket_service import TicketService
from app.repositories.session_repository import SessionRepository

router = APIRouter()
service = TicketService()
session_repo = SessionRepository()


def get_user_role(sessionId):
    user_data = session_repo.get_user_details(sessionId)

    if not user_data:
        raise HTTPException(status_code=401, detail="Invalid session")

    return user_data[1]


# ✅ GET ALL
@router.get("/tickets")
def list_tickets(sessionId: str):

    role = get_user_role(sessionId)

    if role not in ["admin", "support_engineer"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    return service.list_tickets()


# ✅ GET ONE (UUID SAFE)
@router.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: UUID, sessionId: str):

    role = get_user_role(sessionId)

    if role not in ["admin", "support_engineer"]:
        raise HTTPException(status_code=403, detail="Not authorized")

    ticket = service.get_ticket(str(ticket_id))

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


# ✅ ASSIGN
@router.patch("/tickets/{ticket_id}/assign")
def assign_ticket(ticket_id: UUID, sessionId: str):

    role = get_user_role(sessionId)

    success, msg = service.assign_ticket(str(ticket_id), role)

    if not success:
        raise HTTPException(status_code=403, detail=msg)

    return {"message": msg}


# ✅ CLOSE
@router.patch("/tickets/{ticket_id}/close")
def close_ticket(ticket_id: UUID, sessionId: str):

    role = get_user_role(sessionId)

    success, msg = service.close_ticket(str(ticket_id), role)

    if not success:
        raise HTTPException(status_code=403, detail=msg)

    return {"message": msg}