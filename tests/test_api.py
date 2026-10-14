
from fastapi.testclient import TestClient

from app.main import app
from app import main

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ask_returns_answer(monkeypatch):
    monkeypatch.setattr(
        main,
        "answer_question",
        lambda question: {
            "question": question,
            "answer": "Employees receive 20 days of annual leave.",
            "sources": [
                {
                    "document": "company_policy.txt",
                    "excerpt": "Employees receive 20 days of paid annual leave.",
                }
            ],
            "found_evidence": True,
        },
    )

    response = client.post(
        "/ask",
        json={"question": "How many annual leave days are provided?"},
    )

    assert response.status_code == 200
    assert response.json()["found_evidence"] is True
    assert response.json()["sources"][0]["document"] == "company_policy.txt"


def test_ask_rejects_short_question():
    response = client.post("/ask", json={"question": "Hi"})
    assert response.status_code == 422


def test_ingest_txt(monkeypatch):
    monkeypatch.setattr(
        main,
        "chunk_document",
        lambda filename, content: [
            {"text": "Sample text", "source": filename, "chunk_index": 0}
        ],
    )
    monkeypatch.setattr(main, "add_chunks", lambda chunks: len(chunks))

    response = client.post(
        "/ingest",
        files={"file": ("test.txt", b"Sample text", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["chunks_created"] == 1
