from fastapi import FastAPI
from backend.routers.student_routers import router as student_router
from backend.routers.assessment_router import router as assessment_router
from backend.routers.recommendation_router import router as recommendation_router
from backend.routers.degree_router import router as degree_router
from backend.routers.chatbot_router import router as chatbot_router
from backend.routers.rag_router import router as rag_router
from backend.models.create_tables import create_tables

app = FastAPI()
app.include_router(student_router)
app.include_router(assessment_router)
app.include_router(recommendation_router)
app.include_router(degree_router)
app.include_router(chatbot_router)
app.include_router(rag_router)

create_tables()

