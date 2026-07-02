from backend.services.student_services import get_student, save_degree_recommendations
from backend.services.assessment import get_assessment_scores
from backend.services.gemini_services import get_degree_recommendation
from backend.schemas.gemini_recommendation import DegreeRecommendationResponse
from fastapi import APIRouter, HTTPException, Request
from backend.limiter import limiter

router = APIRouter()

@router.get("/api/recommend/degrees/{id}", response_model=DegreeRecommendationResponse, summary="Potential degree generation", description="Takes the student id and gives the recommended degrees for that student based on their responses.")
@limiter.limit("5/minute")
def get_function(id: int, request: Request):
    student_data = get_student(id)
    stream = student_data[3]
    interests = student_data[4].split(", ")
    academic_level = student_data[5]
    keywords = interests
    scores = get_assessment_scores(id)
    try:
        result = get_degree_recommendation(stream,interests,scores,keywords,academic_level)
        save_degree_recommendations(id, result)
        return DegreeRecommendationResponse (**result)
    #Error handling
    except Exception as e:
        print(f"DEGREE ERROR: {str(e)}")
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")