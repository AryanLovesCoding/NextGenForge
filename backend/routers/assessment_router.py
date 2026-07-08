from backend.schemas.assessment import Responses, AssessmentScoresSave
from backend.services.assessment import calculate_scores, assessment_scores
from fastapi import APIRouter
router = APIRouter()

@router.post("/api/assessment", summary="Student assessment scores", description="Posts student assessment scores into the router")
def post_function(response: Responses):
    return calculate_scores(response.responses)

@router.post("/api/assessment/{student_id}/save", summary="Save assessment scores", description="Saves a student's calculated assessment scores to the database")
def save_function(student_id: int, payload: AssessmentScoresSave):
    assessment_scores(student_id, {
        "STEM": payload.STEM,
        "Commerce": payload.Commerce,
        "Humanities": payload.Humanities,
        "Design/Creative Arts": payload.creative
    })
    return {"status": "saved"}