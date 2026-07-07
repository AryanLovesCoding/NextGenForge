from backend.schemas.student import StudentCreate, StudentResponse, StudentInterestsUpdate, StudentAcademicUpdate, StudentIdResponse
from backend.services.student_services import create_student, get_student, update_student_interests, update_student_academic
from fastapi import APIRouter
router = APIRouter()

#Function to receive a StudentCreate object and create a new student and return the student id
@router.post("/api/students", response_model=StudentIdResponse, summary="Create a new student profile", description="Creates a new student record in the database and returns the student ID")
def post_function(student: StudentCreate):
    return {"id": create_student(student)}

#Function to use the student id from the URL and return all information about the student
@router.get("/api/students/{id}", response_model=StudentResponse, summary="Gets all the information of the student", description="Takes ths student id and returns all the information about the student")
def get_function(id: int):
    return get_student(id)

#Function to update a student's interests (subjects + keywords)
@router.patch("/api/students/{id}/interests", summary="Update student interests", description="Updates a student's subjects and career aspiration keywords")
def update_interests_function(id: int, payload: StudentInterestsUpdate):
    update_student_interests(id, payload.subjects, payload.keywords)
    return {"status": "updated"}

#Function to update a student's stream preference and academic level
@router.patch("/api/students/{id}/academic", summary="Update student academic profile", description="Updates a student's stream preference and academic level")
def update_academic_function(id: int, payload: StudentAcademicUpdate):
    update_student_academic(id, payload.stream_preference, payload.academic_level)
    return {"status": "updated"}