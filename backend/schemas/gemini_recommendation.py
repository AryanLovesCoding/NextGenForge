from pydantic import BaseModel

class StreamRecommendationRequest(BaseModel):
    scores: dict
    academic_level: str 
    keywords: list

class StreamRecommendationResponse(BaseModel):
    response: str 