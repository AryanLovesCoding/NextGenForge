from backend.schemas.chatbot import ChatRequest, ChatResponse
from backend.services.gemini_services import get_chat_response
from fastapi import APIRouter, HTTPException
router = APIRouter()

@router.post("/api/chat")
def post_function(request: ChatRequest):
    try:
        result = get_chat_response(request.message, request.chat_history, request.student_context)
        return ChatResponse(response=result)
    #Error handling
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")