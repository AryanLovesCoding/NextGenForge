from fastapi.responses import StreamingResponse
from backend.services.pdf_service import generate_report
from fastapi import APIRouter

router = APIRouter()

@router.get("/api/report/{student_id}")
def get_report(student_id: int):
    buffer = generate_report(student_id)
    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=career_report_{student_id}.pdf"}
    )