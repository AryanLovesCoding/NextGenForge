from fastapi import FastAPI
from backend.routers.student_routers import router
from backend.models.create_tables import create_tables

app = FastAPI()
app.include_router(router)

create_tables()

