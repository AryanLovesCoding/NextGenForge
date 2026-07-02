from backend.schemas.rag_service import RAGRequest, RAGResponse
from backend.services.rag_service import get_rag_response, is_prompt_injection
from backend.services.student_services import save_conversation_turn
from fastapi import APIRouter, HTTPException, Request
from backend.limiter import limiter

router = APIRouter()

@router.post("/api/chat/rag", response_model=RAGResponse, summary="RAG-powered career guidance chat", description="Accepts a user query and chat history, retrieves relevant documents from ChromaDB, and returns a grounded response with source citations")
@limiter.limit("10/minute")
def post_function(payload: RAGRequest, request: Request):
    if is_prompt_injection(payload.query):
        raise HTTPException(status_code=400, detail="Prompt violated our policies. Please try again.")
    try:
        result = get_rag_response(payload.query, payload.stream, payload.chat_history, payload.student_context)
        save_conversation_turn(payload.student_id, "user", payload.query)
        save_conversation_turn(payload.student_id, "assistant", result["response"])
        return RAGResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")