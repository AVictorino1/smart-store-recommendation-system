import sqlite3
from app.database.connection import get_connection

def map_message(row):
    return dict(row)

def get_conversation_history(phone_number: str, limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT role, content 
        FROM conversation_history 
        WHERE phone_number = ? 
        ORDER BY timestamp DESC 
        LIMIT ?
    """, (phone_number, limit))

    rows = cursor.fetchall()
    conn.close()

    # invertís el orden para que quede cronológico
    return [map_message(row) for row in reversed(rows)]

def save_message(phone_number: str, role: str, content: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO conversation_history(phone_number, role, content)
        VALUES (?, ?, ?)
    """, (phone_number, role, content))

    conn.commit()
    conn.close()

def clear_conversation(phone_number: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM conversation_history 
        WHERE phone_number = ?
    """, (phone_number,))

    conn.commit()
    conn.close()