
from pathlib import Path

import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown"}

splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=120,
)


def extract_text(filename: str, content: bytes) -> str:
    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError("Unsupported file type. Upload PDF, TXT, or Markdown.")

    if not content:
        raise ValueError("The uploaded file is empty.")

    if extension == ".pdf":
        with pymupdf.open(stream=content, filetype="pdf") as pdf:
            text = "\n".join(page.get_text() for page in pdf)
    else:
        text = content.decode("utf-8-sig")

    if not text.strip():
        raise ValueError("No readable text found in the document.")

    return text


def chunk_document(filename: str, content: bytes) -> list[dict]:
    text = extract_text(filename, content)
    chunks = splitter.split_text(text)

    return [
        {
            "text": chunk,
            "source": filename,
            "chunk_index": index,
        }
        for index, chunk in enumerate(chunks)
    ]
