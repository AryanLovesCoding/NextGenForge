from backend.schemas.college_comparision import CollegeResponse
from backend.services.college_service import get_colleges
from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter()

@router.get("/api/colleges")
def get_function(stream: Optional[str] = None, state: Optional[str] = None, max_fee: Optional[str] = None):
    try:
        result = get_colleges(stream, state, max_fee)
        return [CollegeResponse(name=r[1], stream=r[2], city=r[3], state=r[4],ranking=r[5], annual_fees=r[6], entrance_exam=r[7],placement_average=r[8], notable_alumni=r[9]) for r in result]
    #Error handling
    except Exception as e:
        print(f"DEGREE ERROR: {str(e)}")
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")
