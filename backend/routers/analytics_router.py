from backend.services.analytics_service import get_analytics_summary
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/api/analytics/summary")
def get_function():
    try:
        result = get_analytics_summary()
        return result
    #Error handling
    except Exception as e:
        print(f"ROADMAP ERROR: {str(e)}")
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {str(e)}")

@router.post("/api/analytics/test-data")
def insert_test_data():
    import sqlite3
    conn = sqlite3.connect('backend/database/nextgenforge.db')
    cursor = conn.cursor()
    test_students = [
        ("Rahul Sharma", "Mumbai", "STEM", "Physics,Maths", "75-90", "Science/PCM"),
        ("Priya Gupta", "Delhi", "Commerce", "Accountancy,Economics", "70-85", "Commerce"),
        ("Arjun Singh", "Bangalore", "Humanities", "History,Political Science", "65-80", "Humanities"),
        ("Sneha Patel", "Chennai", "STEM", "Biology,Chemistry", "85-95", "Science/PCB"),
    ]
    for s in test_students:
        cursor.execute("""INSERT INTO Student (name, city, stream_preference, interests, academic_level, recommended_stream, created_at) 
                         VALUES (?, ?, ?, ?, ?, ?, datetime('now'))""", s)
    conn.commit()
    conn.close()
    return {"message": "Test data inserted"}