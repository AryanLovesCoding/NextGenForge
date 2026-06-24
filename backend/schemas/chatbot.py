from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    chat_history: list[dict]
    student_context: dict

class ChatResponse(BaseModel):
    response: str