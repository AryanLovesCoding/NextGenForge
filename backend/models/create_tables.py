import sqlite3
from backend.database.connection import connect_to_database

#Functino to create tables by creating a connection to database
def create_tables():
    conn = connect_to_database()
    cursor = conn.cursor()

# Student column   
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Student (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            city VARCHAR(255),
            stream_preference VARCHAR(255),
            interests VARCHAR(255),
            academic_level INTEGER,
            created_at TEXT
        )
    """)

#Session table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Session (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            created_at TEXT,
            FOREIGN KEY (student_id) REFERENCES Student(id)
        )
    """)

#ConversationHistory table 
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ConversationHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            role VARCHAR(255),
            message VARCHAR(255),
            timestamp TEXT,
            FOREIGN KEY (session_id) REFERENCES Session(id)
        )
    """)

#Assessment Scores table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS AssessmentScores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            stem_score REAL,
            commerce_score REAL,
            humanities_score REAL,
            creative_score REAL,
            created_at TEXT,
            FOREIGN KEY (student_id) REFERENCES Student(id)
        )
    """)

# Comparision table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS CollegeComparision (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name VARCHAR(255),
                   stream VARCHAR(255),
                   city VARCHAR(255),
                   state VARCHAR(255),
                   ranking INTEGER,
                   annual_fees VARCHAR(255),
                   entrance_exam VARCHAR(255),
                   placement_average VARCHAR(255),
                   notable_alumni TEXT)
    """)

    conn.commit()
    conn.close()
#Checking message
    print("Tables created successfully.")

create_tables()