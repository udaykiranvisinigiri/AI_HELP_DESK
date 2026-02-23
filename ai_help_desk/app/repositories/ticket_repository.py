import uuid
from app.core.database import get_connection


class TicketRepository:

    # ✅ CREATE (UUID FIXED)
    def create_ticket(self, session_id, user_role, module, tier, severity, summary, full_context):

        ticket_id = str(uuid.uuid4())   # 🔥 UUID generated here

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO tickets 
            (ticket_id, session_id, user_role, module, tier, severity, summary, full_context, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'OPEN')
            """,
            (ticket_id, session_id, user_role, module, tier, severity, summary, full_context)
        )

        conn.commit()
        cur.close()
        conn.close()

        return ticket_id


    # ✅ GET ALL
    def get_all_tickets(self):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM tickets ORDER BY created_at DESC")

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows


    # ✅ GET ONE
    def get_ticket_by_id(self, ticket_id):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM tickets WHERE ticket_id=%s", (str(ticket_id),))
        row = cur.fetchone()

        cur.close()
        conn.close()

        return row


    # ✅ ASSIGN
    def assign_ticket(self, ticket_id, assigned_to):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE tickets
            SET assigned_to=%s,
                status='IN_PROGRESS'
            WHERE ticket_id=%s
            """,
            (assigned_to, str(ticket_id))
        )

        conn.commit()
        cur.close()
        conn.close()


    # ✅ CLOSE
    def close_ticket(self, ticket_id, closed_by):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            UPDATE tickets
            SET status='CLOSED',
                closed_by=%s,
                closed_at=NOW()
            WHERE ticket_id=%s
            """,
            (closed_by, str(ticket_id))
        )

        conn.commit()
        cur.close()
        conn.close()