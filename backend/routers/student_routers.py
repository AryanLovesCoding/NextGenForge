from backend.schemas.student import StudentCreate, StudentResponse
from backend.services.student_services import create_student, get_student
from fastapi import APIRouter
router = APIRouter()

#Function to receive a StudentCreate object and create a new student and return the student id
@router.post("/api/students", response_model=StudentResponse, summary="Create a new student profile", description="Creates a new student record in the database and returns the student ID")
def post_function(student: StudentCreate):
    return create_student(student)

#Function to use the student id from the URL and return all information about the student
@router.get("/api/students/{id}", response_model=StudentResponse, summary="Gets all the information of the student", description="Takes ths student id and returns all the information about the student")
def get_function(id: int):
    return get_student(id)