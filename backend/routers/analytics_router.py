from backend.services.analytics_service import get_analytics_summary
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/api/analytics/summary", summary="Analytics for admin dashboard", description="Gets the stats from the router.")
def get_function():
    try:
        result = get_analytics_summary()
        return result
    #Error handling
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")