from fastapi import FastAPI
from backend.routers.student_routers import router as student_router
from backend.routers.assessment_router import router as assessment_router
from backend.routers.recommendation_router import router as recommendation_router
from backend.routers.degree_router import router as degree_router
from backend.routers.chatbot_router import router as chatbot_router
from backend.routers.rag_router import router as rag_router
from backend.routers.roadmap_router import router as roadmap_router
from backend.routers.college_router import router as college_router
from backend.routers.analytics_router import router as analytics_router
from backend.routers.pdf_router import router as pdf_router
from backend.models.create_tables import create_tables


app = FastAPI()
app.include_router(student_router)
app.include_router(assessment_router)
app.include_router(recommendation_router)
app.include_router(degree_router)
app.include_router(chatbot_router)
app.include_router(rag_router)
app.include_router(roadmap_router)
app.include_router(college_router)
app.include_router(analytics_router)
app.include_router(pdf_router)

create_tables()

