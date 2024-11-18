import sqlite3
from contextlib import contextmanager

DATABASE_NAME = "apartments.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS apartments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                address TEXT,
                latitude REAL,
                longitude REAL,
                contact_info TEXT,
                lowest_price REAL,
                times_contacted INTEGER,
                last_updated TIMESTAMP,
                phone_number TEXT,
                notes TEXT,
                is_tracked BOOLEAN,
                rating INTEGER DEFAULT 0
            )
        """)