from app.models.schemas import ChatResponse, GuardrailInfo
from app.repositories.session_repository import SessionRepository
from app.services.guardrail_service import GuardrailService
from app.services.tier_service import TierService
from app.repositories.ticket_repository import TicketRepository
from app.repositories.guardrail_repository import GuardrailRepository
from app.services.rag_service import RAGService


class ChatService:

    def __init__(self):
        self.session_repo = SessionRepository()
        self.guardrail_service = GuardrailService()
        self.tier_service = TierService()
        self.ticket_repo = TicketRepository()
        self.guardrail_repo = GuardrailRepository()
        self.rag_service = RAGService()

    def process_message(self, request):

        history = self.session_repo.get_messages_by_session(request.sessionId)

        user_data = self.session_repo.get_user_details(request.sessionId)

        if not user_data:
            return ChatResponse(
                answer="Invalid session. Please login again.",
                kbReferences=[],
                confidence=0.0,
                tier="TIER_0",
                severity="LOW",
                needsEscalation=False,
                guardrail=GuardrailInfo(blocked=False, reason=None),
                ticketId=None
            )

        user_id, user_role = user_data

        blocked, reason = self.guardrail_service.check(
            request.message,
            user_role
        )

        if blocked:

            full_context = "\n".join(
                [f"{r}: {m}" for r, m, _ in history] +
                [f"{user_role}: {request.message}"]
            )

            ticket_id = self.ticket_repo.create_ticket(
                session_id=request.sessionId,
                user_role=user_role,
                module=None,
                tier="TIER_2",
                severity="HIGH",
                summary=request.message,
                full_context=full_context
            )

            self.guardrail_repo.log_event(
                session_id=request.sessionId,
                reason=reason
            )

            self.session_repo.save_message(
                session_id=request.sessionId,
                user_id=user_id,
                role=user_role,
                message=request.message
            )

            return ChatResponse(
                answer="This request violates platform security policy and cannot be fulfilled.",
                kbReferences=[],
                confidence=1.0,
                tier="TIER_2",
                severity="HIGH",
                needsEscalation=True,
                guardrail=GuardrailInfo(blocked=True, reason=reason),
                ticketId=ticket_id
            )

        self.session_repo.save_message(
            session_id=request.sessionId,
            user_id=user_id,
            role=user_role,
            message=request.message
        )

        previous_failures = sum(
            1 for role, msg, _ in history
            if msg.lower() == request.message.lower()
        )

        if previous_failures >= 1:

            full_context = "\n".join(
                [f"{r}: {m}" for r, m, _ in history]
            )

            ticket_id = self.ticket_repo.create_ticket(
                session_id=request.sessionId,
                user_role=user_role,
                module=None,
                tier="TIER_2",
                severity="HIGH",
                summary=request.message,
                full_context=full_context
            )

            return ChatResponse(
                answer="This issue has been reported multiple times. Escalating to Tier 2 support.",
                kbReferences=[],
                confidence=0.8,
                tier="TIER_2",
                severity="HIGH",
                needsEscalation=True,
                guardrail=GuardrailInfo(blocked=False, reason=None),
                ticketId=ticket_id
            )

        tier, severity, escalate = self.tier_service.classify(
            request.message,
            user_role,
            None
        )

        msg = request.message.lower()

        if "login" in msg or "redirected" in msg:

            browser_keywords = ["chrome", "firefox", "edge", "safari"]
            environment_keywords = ["lab vm", "local machine", "vm"]

            if not any(b in msg for b in browser_keywords) or not any(e in msg for e in environment_keywords):

                return ChatResponse(
                    answer=(
                        "To better assist you, could you please clarify:\n"
                        "1. Which browser are you using?\n"
                        "2. Are you accessing from a lab VM or your local machine?\n"
                        "3. Approximately when did the issue start?"
                    ),
                    kbReferences=[],
                    confidence=0.7,
                    tier=tier,
                    severity=severity,
                    needsEscalation=False,
                    guardrail=GuardrailInfo(blocked=False, reason=None),
                    ticketId=None
                )

        user_messages = [
            m for role, m, _ in history
            if role.lower() == user_role.lower()
        ]

        previous_user_message = user_messages[-1] if user_messages else None

        combined_query = (
            previous_user_message + " " + request.message
            if previous_user_message else request.message
        )

        print("DEBUG combined_query:", combined_query)

        retrieved_chunks = self.rag_service.retrieve(combined_query)

        if not retrieved_chunks:
            return ChatResponse(
                answer="I could not find any relevant information in the knowledge base.",
                kbReferences=[],
                confidence=0.1,
                tier="TIER_0",
                severity="LOW",
                needsEscalation=False,
                guardrail=GuardrailInfo(blocked=False, reason=None),
                ticketId=None
            )

        top_distance = retrieved_chunks[0][3]

        print("DEBUG top_distance:", top_distance)

        if top_distance > 1.2:
            return ChatResponse(
                answer="This query is outside the scope of the CyberLab support system.",
                kbReferences=[],
                confidence=0.2,
                tier="TIER_0",
                severity="LOW",
                needsEscalation=False,
                guardrail=GuardrailInfo(blocked=False, reason=None),
                ticketId=None
            )

        answer = self.rag_service.generate_answer(
            request.message,
            retrieved_chunks,
            history,
            user_role
        )

        confidence = max(min(round(1 - top_distance, 2), 1.0), 0.0)

        ticket_id = None
        if escalate:

            full_context = "\n".join(
                [f"{r}: {m}" for r, m, _ in history]
            )

            ticket_id = self.ticket_repo.create_ticket(
                session_id=request.sessionId,
                user_role=user_role,
                module=None,
                tier=tier,
                severity=severity,
                summary=request.message,
                full_context=full_context
            )

        return ChatResponse(
            answer=answer,
            kbReferences=[
                {"id": c[0], "title": c[1]}
                for c in retrieved_chunks
            ],
            confidence=confidence,
            tier=tier,
            severity=severity,
            needsEscalation=escalate,
            guardrail=GuardrailInfo(blocked=False, reason=None),
            ticketId=ticket_id
        )
