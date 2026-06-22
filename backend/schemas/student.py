from pydantic import BaseModel

#StudentCreate object with all the student's answers
class StudentCreate(BaseModel):
    name: str
    city: str
    stream_preference: str
    interests: list[str]
    academic_level: str

#Student's response with the id and time it was created at
class StudentResponse(BaseModel):
    id: int
    name: str
    city: str
    stream_preference: str
    interests: list[str]
    academic_level: str
    created_at: str