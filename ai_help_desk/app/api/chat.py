from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.chat_services import ChatService

router = APIRouter()

chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):

    return chat_service.process_message(payload)
