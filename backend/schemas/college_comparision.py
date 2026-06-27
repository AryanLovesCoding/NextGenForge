from pydantic import BaseModel
from typing import Optional

class CollegeResponse(BaseModel):
    name: str
    stream: str
    city: str
    state: str
    ranking: int
    annual_fees: str
    entrance_exam: str
    placement_average: str
    notable_alumni: str