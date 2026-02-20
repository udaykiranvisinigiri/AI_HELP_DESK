from openai import OpenAI
from app.repositories.vector_repository import VectorRepository
from app.core.config import OPENAI_API_KEY


class RAGService:

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.vector_repo = VectorRepository()

    def embed_query(self, query: str):

        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )

        return response.data[0].embedding

    def retrieve(self, query: str, k=5):

        embedding = self.embed_query(query)

        results = self.vector_repo.similarity_search(embedding, k)

        filtered = [r for r in results if r[3] < 1.2]

        print("RAW RESULTS:", results)
        print("FILTERED RESULTS:", filtered)

        return filtered

    def generate_answer(self, query: str, retrieved_chunks, conversation_history, user_role: str):

        context = "\n\n".join([chunk[2] for chunk in retrieved_chunks])

        history_text = "\n".join([
            f"{role}: {message}"
            for role, message, _ in conversation_history[-5:]
        ])

        prompt = f"""
You are an internal CyberLab AI Help Desk.

USER ROLE: {user_role}

STRICT RULES:
- Use ONLY the provided KB context.
- Use the KB context to answer as best as possible.
- If partial information exists, provide best possible troubleshooting steps.
- Only say "This is not covered in the knowledge base." if absolutely no relevant information exists.
- Do NOT invent commands, URLs, policies, or procedures.
- If the user already provided clarification details, do NOT ask again.
- Follow role-based restrictions strictly.

CONVERSATION HISTORY:
{history_text}

KB CONTEXT:
{context}

USER QUESTION:
{query}
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content
