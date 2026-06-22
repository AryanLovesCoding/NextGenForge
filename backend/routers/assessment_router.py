from backend.schemas.assessment import Responses
from backend.services.assessment import calculate_scores
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/assessment")
def post_function(response: Responses):
    return calculate_scores(response.responses)
    