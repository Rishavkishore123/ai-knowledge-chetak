
import chromadb

from app.config import settings
from app.embeddings import embeddings


client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_DIR
)

collection = client.get_or_create_collection(
    name="knowledge_documents",
    metadata={"hnsw:space": "cosine"},
)


def add_chunks(chunks: list[dict]) -> int:
    if not chunks:
        return 0

    vectors = embeddings.embed_documents(
        [chunk["text"] for chunk in chunks]
    )

    collection.upsert(
        ids=[
            f'{chunk["source"]}_{chunk["chunk_index"]}'
            for chunk in chunks
        ],
        documents=[chunk["text"] for chunk in chunks],
        embeddings=vectors,
        metadatas=[
            {
                "source": chunk["source"],
                "chunk_index": chunk["chunk_index"],
            }
            for chunk in chunks
        ],
    )

    return len(chunks)


def search_chunks(question: str, top_k: int = 3) -> list[dict]:
    if collection.count() == 0:
        return []

    query_vector = embeddings.embed_query(question)

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=min(top_k, collection.count()),
    )

    matches = []

    for i, document in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]

        matches.append(
            {
                "text": document,
                "source": metadata["source"],
                "chunk_index": metadata["chunk_index"],
                "distance": results["distances"][0][i],
            }
        )

    return matches
