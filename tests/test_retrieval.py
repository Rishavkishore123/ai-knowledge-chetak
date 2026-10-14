
from app.vector_store import add_chunks, search_chunks


def test_add_and_search_chunks():
    chunks = [
        {
            "text": "Employees receive 20 days of paid annual leave.",
            "source": "retrieval_test_policy.txt",
            "chunk_index": 0,
        }
    ]

    add_chunks(chunks)
    results = search_chunks(
        "How many annual leave days are provided?"
    )

    assert results
    assert results[0]["source"] == "retrieval_test_policy.txt"
    assert "20 days" in results[0]["text"]
