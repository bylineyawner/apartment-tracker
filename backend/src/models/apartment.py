# backend/src/models/apartment.py
from dataclasses import dataclass
from datetime import datetime
from math import cos, asin, sqrt

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

    @staticmethod
    def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        p = 0.017453292519943295
        hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
        return 12742 * asin(sqrt(hav))  # 2*R*asin... R = 6371 km

# backend/src/database.py
import sqlite3
from contextlib import contextmanager
from .models.apartment import Apartment

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

    def find_apartments_in_radius(self, lat: float, lon: float, radius_km: float = 5) -> list[Apartment]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Get all apartments - filtering by distance will be done in Python
            cursor.execute("SELECT * FROM apartments")
            apartments = []
            
            for row in cursor.fetchall():
                apt = Apartment(*row)
                distance = Apartment.distance(lat, lon, apt.latitude, apt.longitude)
                if distance <= radius_km:
                    apartments.append(apt)
            
            return apartments

# backend/src/app.py
from flask import Flask, jsonify, request
from flask_cors import CORS
from .database import ApartmentDB

app = Flask(__name__)
CORS(app)
db = ApartmentDB()

@app.route('/api/apartments/search', methods=['POST'])
def search_apartments():
    data = request.json
    apartments = db.find_apartments_in_radius(
        float(data['lat']), 
        float(data['lon']), 
        float(data.get('radius', 5))
    )
    return jsonify([{
        'id': apt.id,
        'name': apt.name,
        'address': apt.address,
        'latitude': apt.latitude,
        'longitude': apt.longitude,
        'lowestPrice': apt.lowest_price,
        'contact_info': apt.contact_info,
        'phone_number': apt.phone_number,
        'rating': apt.rating
    } for apt in apartments])