import sqlite3
from app.database.connection import get_connection

def map_business(row):
    return dict(row)

def get_business_info():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM business_info LIMIT 1")
    row = cursor.fetchone()

    conn.close()

    if row:
        return map_business(row)
    return None

def get_business_schema():
    business = get_business_info()
    return {"trigger_fields": business["trigger_fields"],
        "regenerated_fields": business["regenerated_fields"]}

def update_business_info(field: str, value: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"UPDATE business_info SET {field} = ? WHERE id = 1", (value,))
    conn.commit()
    conn.close()