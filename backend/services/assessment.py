from data.questions import questions
from backend.database.connection import connect_to_database
from datetime import datetime

#Functino to calulate scores based on student response
def calculate_scores(responses):
    scores = {"STEM": 0, "Commerce": 0, "Humanities": 0, "Design/Creative Arts": 0}
    for question, response in zip(questions, responses):
        domain = question["domain"]
        if domain in scores:
            scores[domain]+=response

    for domain in scores:
        scores[domain] /= 25

    return scores

#Function to save the scores vector to database
def assessment_scores(student_id:int, scores):
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = """INSERT INTO AssessmentScores (student_id, stem_score, commerce_score, humanities_score, 
                                    creative_score, created_at) VALUES (?, ?, ?, ?, ?, ?)"""
    values = (student_id, scores["STEM"], scores["Commerce"], scores["Humanities"], 
              scores["Design/Creative Arts"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

def get_assessment_scores(student_id: int):
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = """SELECT * FROM AssessmentScores WHERE student_id = ?"""
    cursor.execute(sql, (student_id,))
    result = cursor.fetchone()
    conn.close()
    return {
    "STEM": result[2],
    "Commerce": result[3],
    "Humanities": result[4],
    "Design/Creative Arts": result[5]
    }

    
            