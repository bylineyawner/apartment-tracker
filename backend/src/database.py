# backend/src/database.py
from contextlib import contextmanager
import sqlite3
from datetime import datetime

class ApartmentDB:
    def __init__(self, db_path="apartments.db"):
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS apartments (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    contact_info TEXT,
                    lowest_price REAL,
                    times_contacted INTEGER DEFAULT 0,
                    last_updated TIMESTAMP,
                    phone_number TEXT,
                    notes TEXT,
                    rating INTEGER DEFAULT 0,
                    is_tracked BOOLEAN DEFAULT FALSE
                )
            """)