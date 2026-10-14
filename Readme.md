# AI Knowledge Assistant

A lightweight Retrieval-Augmented Generation (RAG) application that answers questions from uploaded PDF, TXT, and Markdown documents using semantic retrieval, ChromaDB, and a Groq-hosted LLM.

## Features

- Document ingestion and overlapping text chunking
- Local embeddings using HuggingFace Sentence Transformers
- Persistent vector storage using ChromaDB
- Context-grounded question answering with Groq
- Source document names and supporting evidence excerpts
- Abstention when relevant evidence is unavailable
- FastAPI endpoints with interactive Swagger documentation
- Automated tests and a 10-question evaluation suite
- Docker support

## Architecture

1. **Ingestion:** Extract text from PDF, TXT, or Markdown files.
2. **Chunking:** Split text into overlapping chunks.
3. **Embedding:** Generate vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
4. **Storage:** Store embeddings, text, and metadata in ChromaDB.
5. **Retrieval:** Embed the user's question and retrieve relevant chunks using similarity search.
6. **Generation:** Send retrieved evidence and the question to the Groq LLM.
7. **Response:** Return an answer with source evidence, or abstain when relevant evidence is unavailable.

## Project Structure

```text
app/
  main.py          # FastAPI endpoints
  config.py        # Environment configuration
  ingestion.py     # Document extraction and chunking
  embeddings.py    # Embedding model
  vector_store.py  # ChromaDB operations
  rag.py           # Retrieval and answer generation
  schemas.py       # Request and response models
tests/             # Automated tests
sample_docs/       # Sample documents
evaluation/        # Evaluation questions and script
scripts/           # Utility scripts
Dockerfile
requirements.txt
.env.example
.gitignore
```

## Requirements

- Python 3.11
- A Groq API key
- Docker (optional)

## Setup

Clone the repository and enter the project directory:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd ai-knowledge-assessment
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example` as a template:

```dotenv
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_DB_DIR=./chroma_db
```

Replace the placeholder with your own Groq API key. Never commit `.env` or expose API keys.

## Run the API

Start the application:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API availability |
| POST | `/ingest` | Upload and index a document |
| POST | `/ask` | Ask a question using indexed documents |

### Example Workflow

1. Start the API.
2. Open `/docs` and use `POST /ingest` to upload a document.
3. Use `POST /ask` to ask a question supported by that document.
4. Inspect the answer, `sources`, and `found_evidence` fields.

Example request:

```json
{
  "question": "How many days of paid sick leave are provided?"
}
```

For the included company policy sample, the expected answer is 10 days of paid sick leave per calendar year.

When the indexed documents do not provide relevant evidence, the assistant should acknowledge that it cannot answer from the available information.

## Testing

Run the automated tests:

```bash
python -m pytest tests/ -v
```

## Evaluation

Start the API in one terminal. In another terminal, run:

```bash
python -m evaluation.evaluate
```

The 10-question evaluation suite checks expected answer phrases, source evidence, and abstention behavior.

## Docker

Build the image:

```bash
docker build -t ai-knowledge-assistant .
```

Run the container:

```bash
docker run --rm -p 8000:8000 --env-file .env ai-knowledge-assistant
```

Access the API at http://127.0.0.1:8000/docs.

**Storage note:** The command above removes the container when it stops. Without a mounted volume, indexed ChromaDB data stored inside the container will not persist across container recreation. Upload the documents again after restarting, or configure persistent storage.

## Limitations

- Retrieval quality depends on chunking, embedding similarity, and the relevance threshold.
- Prompting and relevance filtering reduce but do not eliminate unsupported LLM responses.
- Evaluation uses expected-term checks rather than a comprehensive semantic judge.
- The embedding model requires an initial download.
- Scanned PDFs may require OCR if they contain no extractable text.
- Authentication and multi-user access control are not implemented; this is a demonstration project.

## Security

- Keep `.env` and API keys out of version control.
- Use `.env.example` with placeholder values only.
- Do not commit `.venv/`, `__pycache__/`, or local ChromaDB data.
- Never expose API keys in source code, screenshots, logs, or public repositories.
