from backend.schemas.student import StudentCreate
from backend.services.student_services import create_student, get_student
from fastapi import APIRouter
router = APIRouter()

#Function to receive a StudentCreate object and create a new student and return the student id
@router.post("/api/students")
def post_function(student: StudentCreate):
    return create_student(student)

#Function to use the student id from the URL and return all information about the student
@router.get("/api/students/{id}")
def get_function(id: int):
    return get_student(id)