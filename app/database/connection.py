import sqlite3
from app.database.init_db import DB_PATH

def get_connection():
    return sqlite3.connect(DB_PATH)
