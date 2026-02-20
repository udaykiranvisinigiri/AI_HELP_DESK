from app.core.database import get_connection


class GuardrailRepository:

    def log_event(self, session_id: str, reason: str):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO guardrail_events (session_id, reason)
            VALUES (%s, %s)
            """,
            (session_id, reason)
        )

        conn.commit()
        cur.close()
        conn.close()
