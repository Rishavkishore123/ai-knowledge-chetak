
import pytest

from app.ingestion import extract_text, chunk_document


def test_extract_txt():
    text = extract_text(
        "policy.txt",
        b"Employees receive 20 days of annual leave.",
    )
    assert "20 days" in text


def test_extract_markdown():
    text = extract_text("guide.md", b"# Product Guide\nSemantic search")
    assert "Semantic search" in text


def test_reject_unsupported_file():
    with pytest.raises(ValueError):
        extract_text("image.png", b"image content")


def test_reject_empty_file():
    with pytest.raises(ValueError):
        extract_text("empty.txt", b"")


def test_chunk_document():
    chunks = chunk_document("policy.txt", b"Company policy. " * 100)
    assert len(chunks) > 1
    assert chunks[0]["source"] == "policy.txt"
    assert "text" in chunks[0]
