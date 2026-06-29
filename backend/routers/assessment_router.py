from backend.schemas.assessment import Responses
from backend.services.assessment import calculate_scores
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/assessment", summary="Student assessment scores", description="Posts student assessment scores into the router")
def post_function(response: Responses):
    return calculate_scores(response.responses)
    