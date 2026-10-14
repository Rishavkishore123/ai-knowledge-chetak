
from pydantic import BaseModel, Field


class IngestResponse(BaseModel):
    filename: str
    chunks_created: int
    message: str


class QuestionRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)


class SourceEvidence(BaseModel):
    document: str
    excerpt: str


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceEvidence] = Field(default_factory=list)
    found_evidence: bool
