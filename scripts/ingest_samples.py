
from pathlib import Path

from app.ingestion import chunk_document
from app.vector_store import add_chunks


DOCS_DIR = Path("sample_docs")


def main():
    print("Starting document ingestion...")

    if not DOCS_DIR.exists():
        print(f"ERROR: Directory not found: {DOCS_DIR.resolve()}")
        return

    files = [
        path for path in DOCS_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".pdf", ".txt", ".md", ".markdown"}
    ]

    if not files:
        print(f"No supported documents found in {DOCS_DIR.resolve()}")
        return

    all_chunks = []

    for path in files:
        try:
            chunks = chunk_document(path.name, path.read_bytes())
            all_chunks.extend(chunks)
            print(f"{path.name}: {len(chunks)} chunks")
        except Exception as exc:
            print(f"Failed to process {path.name}: {exc}")

    if not all_chunks:
        print("No chunks created. Check the errors above.")
        return

    count = add_chunks(all_chunks)
    print(f"Successfully indexed {count} chunks.")


if __name__ == "__main__":
    main()
