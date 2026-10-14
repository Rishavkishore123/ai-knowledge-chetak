
from groq import Groq

from app.config import settings
from app.vector_store import search_chunks

client = Groq(api_key=settings.GROQ_API_KEY)

# Tune this threshold using your sample documents and evaluation questions.
MAX_COSINE_DISTANCE = 0.55


def answer_question(question: str) -> dict:
    results = search_chunks(question, top_k=3)

    # ChromaDB returns cosine distance because the collection uses cosine space.
    relevant = [
        item for item in results
        if item["distance"] <= MAX_COSINE_DISTANCE
    ]

    if not relevant:
        return {
            "question": question,
            "answer": (
                "The provided documents do not contain enough "
                "information to answer this question."
            ),
            "sources": [],
            "found_evidence": False,
        }

    context = "\n\n".join(
        f"Source: {item['source']}\n"
        f"Excerpt: {item['text']}"
        for item in relevant
    )

    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a document-grounded knowledge assistant. "
                    "Answer only using the supplied evidence. "
                    "Do not use outside knowledge or invent facts. "
                    "If the evidence does not fully answer the question, "
                    "say that the information is unavailable in the "
                    "provided documents. Be concise."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {question}\n\n"
                    f"Evidence:\n{context}\n\n"
                    "Answer using only this evidence."
                ),
            },
        ],
    )

    answer = response.choices[0].message.content or (
        "The provided documents do not contain enough information "
        "to answer this question."
    )

    return {
        "question": question,
        "answer": answer,
        "sources": [
            {
                "document": item["source"],
                "excerpt": item["text"],
            }
            for item in relevant
        ],
        "found_evidence": True,
    }
