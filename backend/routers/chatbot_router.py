from backend.schemas.chatbot import ChatRequest, ChatResponse
from backend.services.gemini_services import get_chat_response
from fastapi import APIRouter, HTTPException, Request
from backend.limiter import limiter
router = APIRouter()

@router.post("/api/chat", response_model=ChatResponse, summary="Gemini powered chatbot", description="Gives chat responses in the form of a chatbot.")
@limiter.limit("5/minute")
def post_function(payload: ChatRequest, request: Request):
    try:
        result = get_chat_response(payload.message, payload.chat_history, payload.student_context)
        return ChatResponse(response=result)
    #Error handling
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")