from backend.schemas.gemini_recommendation import StreamRecommendationResponse, StreamRecommendationRequest
from backend.services.gemini_services import get_stream_recommendation
from fastapi import APIRouter, HTTPException
router = APIRouter()

@router.post("/api/recommend/stream")
def post_function(request: StreamRecommendationRequest):
    try:
        result = get_stream_recommendation(request.scores, request.academic_level, request.keywords)
        return StreamRecommendationResponse(response=result)
    #Error handling
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")