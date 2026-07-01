import sqlite3
import json
from datetime import datetime
from backend.database.connection import connect_to_database
from backend.schemas.student import StudentCreate

# Function to create a new student of the type StudentCreate. 
def create_student (student: StudentCreate):
    """
    Creates a new student object

    Args: student(StudentCreate): a student object of the type StudentCreate from schema

    Returns: the student_id of the new student created 
    """
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
    cursor.execute(
    "INSERT INTO Session (student_id, created_at) VALUES (?, ?)",
    (student_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    cursor.close()
    conn.close()
    return student_id

# Function to retrieve the student's information once provided with the student id.
def get_student(id: int):
    """
    Retrieve the student's information once provided with the student id

    Args: id(int): The student's unique identifier

    Returns: all student data from their responses
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = """SELECT * FROM Student WHERE id = ?"""
    cursor.execute(sql,(id,))
    value = cursor.fetchone()
    conn.close()
    return value

def update_student_interests(student_id, subjects, keywords):
    """
    Updates the student interests with subjects and keywords

    Args: 
        student_id(int): The student's unique identifier
        subjects: list of subjects the student enjoys
        keywords: list of career aspiration keywords

    Returns: None
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = """UPDATE Student SET interests = ? WHERE id = ?"""
    value = ", ".join(subjects + keywords)
    cursor.execute(sql, (value, student_id))
    conn.commit()
    conn.close()

def save_conversation_turn(student_id: int, role: str, message: str):
    """
    Saves the conversation after every thread in ConversationHistory database

    Args: 
        student_id(int): The student's unique identifier
        role(str): 'User' or 'AI' based on who's sending the message
        message(str): user query or AI response

    Returns: None
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = """INSERT INTO ConversationHistory (session_id, role, message, timestamp)
    Values (?, ?, ?, ?)"""
    values = (student_id, role, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cursor.execute(sql,values)
    conn.commit()
    cursor.close()
    conn.close()

def update_recommended_stream(student_id, stream):
    """
    Saves the recommended stream in Student Database

    Args: 
        student_id(int): The student's unique identifier
        stream: the stream recommended by Gemini

    Returns: None
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = """UPDATE Student SET recommended_stream = ? WHERE id = ?"""
    values = (stream, student_id)
    cursor.execute(sql,values)
    conn.commit()
    conn.close()

def save_degree_recommendations(student_id, degrees):
    """
    Saves the recommended degress in Student Database

    Args:
        student_id(int): The student's unique identifier
        degrees: JSON string with degrees
    
    Returns: None
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Student SET degree_recommendations = ? WHERE id = ?", 
               (json.dumps(degrees), student_id)) 
    conn.commit()
    conn.close()

def save_stream_justification(student_id: int, justification: str):
    """
    Saves Gemini stream justification to Student table

    Args:
        student_id(int): The student's unique identifier
        justification(str): justification of why the student was suggested that stream

    Returns: None
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Student SET stream_justification = ? WHERE id = ?", (justification, student_id))
    conn.commit()
    conn.close()

def save_roadmap(student_id: int, roadmap: dict):
    """
    Saves Gemini roadmap to Student table
    
    Args:
        student_id(int): The student's unique identifier
        roadmap(dict): the roadmap the student should take based on their recomended career,
    
    Returns: None
     """
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("UPDATE Student SET roadmap = ? WHERE id = ?", (json.dumps(roadmap), student_id))
    conn.commit()
    conn.close()

def update_student_academic(student_id, stream_preference, academic_level):
    conn = connect_to_database()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Student
        SET stream_preference = ?, academic_level = ?
        WHERE id = ?
    """, (stream_preference, academic_level, student_id))

    conn.commit()
    cursor.close()
    conn.close()

