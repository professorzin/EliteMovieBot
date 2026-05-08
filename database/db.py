import sqlite3
from config import DATABASE_NAME

def connect():
    return sqlite3.connect(DATABASE_NAME, check_same_thread=False)

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        plan TEXT,
        expiry INTEGER,
        used INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS files(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        message_id INTEGER,
        file_name TEXT,
        file_unique_id TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings(
        key TEXT PRIMARY KEY,
        value TEXT
    )
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_unique
    ON files(file_unique_id)
    """)

    cur.execute("""
    CREATE INDEX IF NOT EXISTS idx_name
    ON files(file_name)
    """)

    conn.commit()
    conn.close()
