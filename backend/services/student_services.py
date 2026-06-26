import sqlite3
from datetime import datetime
from backend.database.connection import connect_to_database
from backend.schemas.student import StudentCreate

# Function to create a new student of the type StudentCreate. 
def create_student (student: StudentCreate):
    conn = connect_to_database()
    cursor = conn.cursor()
    #We use ??? to protect against corruption
    sql = """INSERT INTO Student (name, city, stream_preference, interests, academic_level, created_at) 
         VALUES (?, ?, ?, ?, ?, ?)"""
    #SQL doesn't allow tuples so we use the .join() function
    values = (student.name, student.city, student.stream_preference, ", ".join(student.interests), 
              student.academic_level, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cursor.execute(sql,values)
    student_id = cursor.lastrowid
    conn.commit()
    cursor.close()
    conn.close()
    return student_id

# Function to retrieve the student's information once provided with the student id.
def get_student(id: int):
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = """SELECT * FROM Student WHERE id = ?"""
    cursor.execute(sql,(id,))
    value = cursor.fetchone()
    conn.close()
    return value

def update_student_interests(student_id, subjects, keywords):
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = """UPDATE Student SET interests = ? WHERE id = ?"""
    value = ", ".join(subjects + keywords)
    cursor.execute(sql, (value, student_id))
    conn.commit()
    conn.close()


