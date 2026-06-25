from pydantic import BaseModel
from typing import Optional

class RAGRequest(BaseModel):
    query: str
    stream: Optional[str] = None

class RAGResponse (BaseModel):
    response: str
    sources: list[str]