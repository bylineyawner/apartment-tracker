from dataclasses import dataclass
from datetime import datetime
import folium
from typing import Dict, List
import sqlite3
import requests
from flask import Flask, render_template, jsonify, request
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

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
    is_tracked: bool = False

class ApartmentTracker:
    def __init__(self, db_path="apartments.db"):
        self.conn = sqlite3.connect(db_path)
        self.setup_database()
        self.geolocator = Nominatim(user_agent="apartment_tracker")
        
    def setup_database(self):
        cursor = self.conn.cursor()
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
                is_tracked BOOLEAN
            )
        """)
        self.conn.commit()

    def add_apartment(self, apartment: Apartment):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO apartments 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            apartment.id, apartment.name, apartment.address,
            apartment.latitude, apartment.longitude, apartment.contact_info,
            apartment.lowest_price, apartment.times_contacted,
            apartment.last_updated, apartment.phone_number,
            apartment.notes, apartment.is_tracked
        ))
        self.conn.commit()

    def get_apartments_in_radius(self, center_lat: float, center_lon: float, radius_km: float) -> List[Apartment]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM apartments")
        apartments = []
        
        for row in cursor.fetchall():
            apt = Apartment(*row)
            distance = geodesic(
                (center_lat, center_lon),
                (apt.latitude, apt.longitude)
            ).kilometers
            
            if distance <= radius_km:
                apartments.append(apt)
                
        return apartments

    def calculate_commute(self, start_lat: float, start_lon: float, 
                         end_lat: float, end_lon: float) -> Dict:
        # Using OpenStreetMap Routing Machine API (OSRM)
        url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}"
        response = requests.get(url)
        data = response.json()
        
        if data["code"] == "Ok":
            route = data["routes"][0]
            return {
                "distance_km": route["distance"] / 1000,
                "duration_minutes": route["duration"] / 60
            }
        return None

app = Flask(__name__)
tracker = ApartmentTracker()

@app.route('/map')
def show_map():
    center_lat = request.args.get('lat', 37.7749)  # Default to San Francisco
    center_lon = request.args.get('lon', -122.4194)
    radius = request.args.get('radius', 5)
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=13)
    
    apartments = tracker.get_apartments_in_radius(center_lat, center_lon, radius)
    
    for apt in apartments:
        popup_html = f"""
            <b>{apt.name}</b><br>
            Address: {apt.address}<br>
            Price: ${apt.lowest_price:,.2f}<br>
            Phone: {apt.phone_number}<br>
            <button onclick="toggleTracking({apt.id})">
                {'Remove from' if apt.is_tracked else 'Add to'} Tracker
            </button>
        """
        
        folium.Marker(
            [apt.latitude, apt.longitude],
            popup=popup_html,
            icon=folium.Icon(color='red' if apt.is_tracked else 'blue')
        ).add_to(m)
    
    return m._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)