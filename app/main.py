
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.ingestion import chunk_document
from app.vector_store import add_chunks
from app.rag import answer_question
from app.schemas import (
    IngestResponse,
    QuestionRequest,
    QuestionResponse,
)

app = FastAPI(
    title="AI Knowledge Assistant",
    description="A document-grounded question-answering API",
    version="1.0.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ingest", response_model=IngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name

    if not filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    try:
        content = await file.read()
        chunks = chunk_document(filename, content)
        count = add_chunks(chunks)

        return IngestResponse(
            filename=filename,
            chunks_created=count,
            message="Document indexed successfully",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Document ingestion failed",
        ) from exc


@app.post("/ask", response_model=QuestionResponse)
def ask_question(request: QuestionRequest):
    try:
        return answer_question(request.question)
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Question answering failed. Check the LLM service and configuration.",
        ) from exc
