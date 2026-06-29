from backend.database.connection import connect_to_database

def get_analytics_summary():
    """
    Retrieve analytics data for admin dahsboard

    Args: None

    Returns: a list of data to be displayed on admin page     
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Student")
    total_students = cursor.fetchone()[0]
    cursor.execute("SELECT stream_preference, COUNT(*) FROM Student GROUP BY stream_preference")
    stream_preference_distribution = cursor.fetchall()
    cursor.execute("SELECT recommended_stream, COUNT(*) FROM Student GROUP BY recommended_stream")
    recommended_stream_distribution = cursor.fetchall()
    cursor.execute("SELECT message FROM ConversationHistory WHERE role = 'user'")
    messages = cursor.fetchall()
    cursor.execute("SELECT DATE(created_at), COUNT(*) FROM Session GROUP BY DATE(created_at)")
    daily_sessions = cursor.fetchall()
    conn.close()
    return {
        "total_students": total_students,
        "stream_preference_distribution": stream_preference_distribution,
        "recommended_stream_distribution": recommended_stream_distribution,
        "messages": messages,
        "daily_sessions": daily_sessions
    }