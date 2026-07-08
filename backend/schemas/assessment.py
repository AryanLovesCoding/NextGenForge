from pydantic import BaseModel

class Responses (BaseModel):
    responses: list[int]

class AssessmentScoresSave(BaseModel):
    STEM: float
    Commerce: float
    Humanities: float
    creative: float