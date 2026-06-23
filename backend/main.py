from fastapi import FastAPI
from backend.routers.student_routers import router as student_router
from backend.routers.assessment_router import router as assessment_router
from backend.routers.recommendation_router import router as recommendation_router
from backend.models.create_tables import create_tables

app = FastAPI()
app.include_router(student_router)
app.include_router(assessment_router)
app.include_router(recommendation_router)

create_tables()

