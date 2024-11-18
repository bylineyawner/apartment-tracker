# backend/src/models/apartment.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Apartment:
    id: int
    name: str
    address: str
    latitude: float
    longitude: float
    contact_info: str
    lowest_price: float
    times_contacted: int
    last_updated: datetime
    phone_number: str
    notes: str
    rating: int = 0
    is_tracked: bool = False

# backend/src/database.py
import sqlite3
from contextlib import contextmanager
from .models.apartment import Apartment

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

# backend/src/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import folium
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
from .database import get_db, init_db
from .models.apartment import Apartment

app = Flask(__name__)
CORS(app)

@app.route('/apartments', methods=['GET'])
def get_apartments():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM apartments")
        apartments = [Apartment(*row) for row in cursor.fetchall()]
        return jsonify([vars(apt) for apt in apartments])

@app.route('/update_rating', methods=['POST'])
def update_rating():
    data = request.json
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE apartments 
            SET rating = ? 
            WHERE id = ?
        """, (data['rating'], data['id']))
        return jsonify({"success": True})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)