import os
import uuid
from openai import OpenAI
from app.repositories.vector_repository import VectorRepository
from app.core.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def chunk_text(text, chunk_size=300):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield " ".join(words[i:i + chunk_size])


def ingest():

    repo = VectorRepository()
    kb_folder = "kb"

    for file in os.listdir(kb_folder):

        if not file.endswith(".md"):
            continue

        path = os.path.join(kb_folder, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        print(f"Ingesting: {file}")

        chunks = list(chunk_text(content))

        for chunk in chunks:

            embedding = embed_text(chunk)

            repo.insert_chunk(
                chunk_id=str(uuid.uuid4()),
                title=file,
                content=chunk,
                embedding=embedding
            )

    print("Ingestion completed!")


if __name__ == "__main__":
    ingest()
