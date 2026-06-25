from backend.schemas.rag_service import RAGRequest, RAGResponse
from backend.services.rag_service import get_rag_response
from fastapi import APIRouter, HTTPException
router = APIRouter()

@router.post("/api/chat/rag")
def post_function(request: RAGRequest):
    try:
        result = get_rag_response(request.query, request.stream)
        return RAGResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")