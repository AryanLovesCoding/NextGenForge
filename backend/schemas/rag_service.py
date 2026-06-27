from pydantic import BaseModel
from typing import Optional

class RAGRequest(BaseModel):
    query: str
    stream: Optional[str] = None
    chat_history: list[dict] = []
    student_id: int

class RAGResponse (BaseModel):
    response: str
    sources: list[str]