from backend.schemas.college_comparision import CollegeResponse
from backend.database.connection import connect_to_database
from functools import lru_cache

@lru_cache(maxsize=128)
def get_colleges(stream=None, state=None, max_fee=None):
    """
    Gets the colleges based on the filters required by the student

    Args: 
        stream(str): if a student wants to filter by stream otherwise None
        stream(str): if a student wants to filter by stata otherwise None
        max_fee(str): if a student wants to filter by maximum fees otherwise None

    Returns: list of all the colleges which satisfy the filters    
    """
    conn = connect_to_database()
    cursor = conn.cursor()
    sql = "SELECT * FROM CollegeComparision"
    conditions = []
    values = []
    if stream:
        conditions.append("stream = ?")
        values.append(stream)
    if state:
        conditions.append("state = ?")
        values.append(state)
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    cursor.execute(sql, values)
    results = cursor.fetchall()
    if max_fee:
        results = [r for r in results if int(r[6].replace(",", "")) <= int(max_fee)]
    cursor.close()
    conn.close()
    return results

    
    