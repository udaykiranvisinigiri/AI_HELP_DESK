import uuid
from app.core.database import get_connection

class TicketRepository:

    def create_ticket(
        self,
        session_id: str,
        user_role: str,
        module: str,
        tier: str,
        severity: str,
        summary: str,
        full_context: str
    ):

        ticket_id = str(uuid.uuid4())

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO tickets 
            (ticket_id, session_id, user_role, module, tier, severity, summary, full_context)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                ticket_id,
                session_id,
                user_role,
                module,
                tier,
                severity,
                summary,
                full_context
            )
        )

        conn.commit()
        cur.close()
        conn.close()

        return ticket_id
