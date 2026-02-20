from app.core.database import get_connection


class MetricsRepository:

    def get_total_sessions(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(DISTINCT session_id) FROM sessions;")
        result = cur.fetchone()[0]

        cur.close()
        conn.close()

        return result

    def get_total_tickets(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM tickets;")
        result = cur.fetchone()[0]

        cur.close()
        conn.close()

        return result

    def get_guardrail_count(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM guardrail_events;")
        result = cur.fetchone()[0]

        cur.close()
        conn.close()

        return result

    def get_tickets_by_tier(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT tier, COUNT(*)
            FROM tickets
            GROUP BY tier;
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return dict(rows)
