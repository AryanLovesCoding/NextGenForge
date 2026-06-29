from backend.schemas.rag_service import RAGRequest, RAGResponse
from backend.services.rag_service import get_rag_response
from backend.services.student_services import save_conversation_turn
from fastapi import APIRouter, HTTPException
router = APIRouter()

@router.post("/api/chat/rag", response_model=RAGResponse, summary="RAG-powered career guidance chat", description="Accepts a user query and chat history, retrieves relevant documents from ChromaDB, and returns a grounded response with source citations")
def post_function(request: RAGRequest):
    try:
        result = get_rag_response(request.query, request.stream, request.chat_history)
        save_conversation_turn(request.student_id, "user", request.query)
        save_conversation_turn(request.student_id, "assistant", result["response"])
        return RAGResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")