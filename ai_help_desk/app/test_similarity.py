from openai import OpenAI
from repositories.vector_repository import VectorRepository
from core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def test_query(query):

    repo = VectorRepository()

    print(f"\nQuery: {query}\n")

    embedding = embed_text(query)

    results = repo.similarity_search(embedding, k=3)

    for r in results:
        print("ID:", r[0])
        print("Title:", r[1])
        print("-" * 50)


if __name__ == "__main__":
    test_query("I keep getting redirected to login page")
