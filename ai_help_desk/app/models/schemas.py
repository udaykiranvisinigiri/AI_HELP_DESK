from pydantic import BaseModel
from typing import List, Optional


class ChatContext(BaseModel):
    module: Optional[str] = None
    channel: Optional[str] = None


class ChatRequest(BaseModel):
    sessionId: str
    message: str
    context: Optional[ChatContext] = None


class KBReference(BaseModel):
    id: str
    title: str


class GuardrailInfo(BaseModel):
    blocked: bool
    reason: Optional[str]


class ChatResponse(BaseModel):
    answer: str
    kbReferences: List[KBReference]
    confidence: float
    tier: str
    severity: str
    needsEscalation: bool
    guardrail: GuardrailInfo
    ticketId: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
    

