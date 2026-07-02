from pydantic import BaseModel, Field
from typing import Optional

class RAGRequest(BaseModel):
    query: str = Field(..., max_length= 500)
    stream: Optional[str] = None
    chat_history: list[dict] = []
    student_id: int
    student_context: dict = {}

class RAGResponse (BaseModel):
    response: str
    sources: list[str]