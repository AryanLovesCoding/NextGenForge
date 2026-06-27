from pydantic import BaseModel
from typing import Optional

class RoadmapResponse(BaseModel):
    recommended_stream: str
    class_11_12_preparation: str
    entrance_exam_timeline: list[dict]
    undergraduate_milestones: list[dict]
    skill_development: list
    internship_milestones: str
    industry_entry_pathway: str