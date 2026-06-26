from pydantic import BaseModel
from typing import Optional

class StreamRecommendationRequest(BaseModel):
    scores: dict
    academic_level: str 
    keywords: list

class StreamRecommendationResponse(BaseModel):
    recommended_stream: str
    justification: str
    alternative_stream: Optional[str] = None

class DegreeItem(BaseModel):
    degree_name: str
    description: str
    career_pathways: list[str]
    entrance_exams: list[str]
    timeline: str

class DegreeRecommendationRequest(BaseModel):
    scores: dict
    interests: list
    stream: str

class DegreeRecommendationResponse(BaseModel):
    degrees: list[DegreeItem]