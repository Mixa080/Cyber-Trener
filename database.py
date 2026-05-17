import pyodbc
from config import DB_CONNECTION_STRING

def get_db_connection():
    try:
        return pyodbc.connect(DB_CONNECTION_STRING, timeout=3)
    except Exception:
        return None
