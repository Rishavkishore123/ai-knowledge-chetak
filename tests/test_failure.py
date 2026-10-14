
from fastapi.testclient import TestClient

from app.main import app
from app import main

client = TestClient(app)


def test_ingest_rejects_unsupported_file():
    response = client.post(
        "/ingest",
        files={"file": ("image.png", b"content", "image/png")},
    )
    assert response.status_code == 400


def test_llm_failure_returns_error(monkeypatch):
    def fail(question):
        raise RuntimeError("LLM unavailable")

    monkeypatch.setattr(main, "answer_question", fail)

    response = client.post(
        "/ask",
        json={"question": "How many annual leave days are provided?"},
    )

    assert response.status_code == 502
