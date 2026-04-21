from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=3)


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    num_chunks: int
