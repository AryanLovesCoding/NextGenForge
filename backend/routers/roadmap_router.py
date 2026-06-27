from backend.services.student_services import get_student
from backend.services.assessment import get_assessment_scores
from backend.services.gemini_services import get_roadmap
from backend.schemas.roadmap import RoadmapResponse
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/api/roadmap/{student_id}")
def get_function(student_id: int):
    student_data = get_student(student_id)
    stream = student_data[3]
    interests = student_data[4].split(", ")
    keywords = interests
    academic_level = student_data[5]
    scores = get_assessment_scores(student_id)
    try:
        result = get_roadmap(stream, interests, keywords, academic_level, scores)
        return RoadmapResponse (**result)
    #Error handling
    except Exception as e:
        print(f"ROADMAP ERROR: {str(e)}")
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
