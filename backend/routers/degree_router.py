from backend.services.student_services import get_student
from backend.services.assessment import get_assessment_scores
from backend.services.gemini_services import get_degree_recommendation
from backend.schemas.gemini_recommendation import DegreeRecommendationResponse
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/api/recommend/degrees/{id}")
def get_function(id: int):
    student_data = get_student(id)
    stream = student_data[3]
    interests = student_data[4].split(", ")
    scores = get_assessment_scores(id)
    try:
        result = get_degree_recommendation(stream, interests, scores)
        return DegreeRecommendationResponse (**result)
    #Error handling
    except Exception as e:
        print(f"DEGREE ERROR: {str(e)}")
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")