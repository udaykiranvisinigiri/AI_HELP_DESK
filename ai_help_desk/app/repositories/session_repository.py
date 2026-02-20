from app.core.database import get_connection


class SessionRepository:

    def save_message(self, session_id: str, user_id: str, role: str, message: str):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO sessions (session_id, user_id, role, message)
            VALUES (%s, %s, %s, %s)
            """,
            (session_id, user_id, role, message)
        )

        conn.commit()
        cur.close()
        conn.close()

    def get_messages_by_session(self, session_id: str):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT role, message, timestamp
            FROM sessions
            WHERE session_id = %s
            ORDER BY timestamp ASC
            """,
            (session_id,)
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows

    def get_user_details(self, session_id: str):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT user_id, role
            FROM sessions
            WHERE session_id = %s
            LIMIT 1
            """,
            (session_id,)
        )

        row = cur.fetchone()

        cur.close()
        conn.close()

        return row
