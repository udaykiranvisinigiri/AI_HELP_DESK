from app.core.database import get_connection


class VectorRepository:

    def insert_chunk(self, chunk_id, title, content, embedding):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO kb_chunks (id, title, content, embedding)
            VALUES (%s, %s, %s, %s)
            """,
            (chunk_id, title, content, embedding)
        )

        conn.commit()
        cur.close()
        conn.close()

    def similarity_search(self, embedding, k=3):

        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, title, content,
                embedding <-> %s::vector AS distance
            FROM kb_chunks
            ORDER BY embedding <-> %s::vector
            LIMIT %s
            """,
            (embedding, embedding, k)
        )

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return rows
