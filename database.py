import pyodbc
from config import DB_CONNECTION_STRING

def get_db_connection():
    try:
        conn = pyodbc.connect(DB_CONNECTION_STRING, timeout=3)
        _ensure_columns(conn)
        return conn
    except Exception as e:
        print(f"DB connection error: {e}")
        return None

def _ensure_columns(conn):
    try:
        c = conn.cursor()
        c.execute("""
            IF COL_LENGTH('users', 'password_hash') IS NULL
            BEGIN
                ALTER TABLE users ADD password_hash NVARCHAR(255)
            END
        """)
        c.execute("""
            IF COL_LENGTH('workouts', 'dumbbell_weight_kg') IS NULL
            BEGIN
                ALTER TABLE workouts ADD dumbbell_weight_kg INT
            END
        """)
        conn.commit()
    except Exception as e:
        print(f"Migration error: {e}")
