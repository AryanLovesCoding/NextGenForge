from backend.schemas.gemini_recommendation import StreamRecommendationResponse, StreamRecommendationRequest
from backend.services.gemini_services import get_stream_recommendation
from backend.services.student_services import update_recommended_stream, save_stream_justification
from fastapi import APIRouter, HTTPException, Request
from backend.limiter import limiter
router = APIRouter()

@router.post("/api/recommend/stream", response_model=StreamRecommendationResponse, summary="Creates the recommended stream for the student", description="Gives the recommended stream")
@limiter.limit("5/minute")
def post_function(payload: StreamRecommendationRequest, request: Request):
    try:
        result = get_stream_recommendation(payload.scores, payload.academic_level, payload.keywords)
        update_recommended_stream(payload.student_id, result['recommended_stream'])
        save_stream_justification(payload.student_id, result['justification'])
        return StreamRecommendationResponse(**result)
    #Error handling
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")