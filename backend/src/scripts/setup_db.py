# backend/src/scripts/setup_db.py
import sqlite3
from datetime import datetime
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import ApartmentDB

SAMPLE_APARTMENTS = [
    {
        'name': 'Sunny Heights',
        'address': '123 Main St, San Francisco, CA',
        'latitude': 37.7749,
        'longitude': -122.4194,
        'contact_info': 'John Manager (415-555-0123)',
        'lowest_price': 2500,
        'times_contacted': 0,
        'last_updated': datetime.now(),
        'phone_number': '415-555-0123',
        'notes': 'Great views, new appliances',
        'rating': 4,
        'is_tracked': False
    },
    {
        'name': 'Marina View',
        'address': '456 Bay St, San Francisco, CA',
        'latitude': 37.7833,
        'longitude': -122.4167,
        'contact_info': 'Sarah Smith (415-555-0124)',
        'lowest_price': 3200,
        'times_contacted': 0,
        'last_updated': datetime.now(),
        'phone_number': '415-555-0124',
        'notes': 'Close to Marina, parking included',
        'rating': 3,
        'is_tracked': False
    },
    {
        'name': 'Mission Modern',
        'address': '789 Valencia St, San Francisco, CA',
        'latitude': 37.7599,
        'longitude': -122.4215,
        'contact_info': 'Mike Jones (415-555-0125)',
        'lowest_price': 2800,
        'times_contacted': 0,
        'last_updated': datetime.now(),
        'phone_number': '415-555-0125',
        'notes': 'New building, great restaurants nearby',
        'rating': 5,
        'is_tracked': False
    }
]

def populate_database():
    db = ApartmentDB()
    with db.get_connection() as conn:
        cursor = conn.cursor()
        
        # Clear existing data
        cursor.execute("DELETE FROM apartments")
        
        # Insert sample data
        for apt in SAMPLE_APARTMENTS:
            cursor.execute("""
                INSERT INTO apartments (
                    name, address, latitude, longitude, contact_info,
                    lowest_price, times_contacted, last_updated,
                    phone_number, notes, rating, is_tracked
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                apt['name'], apt['address'], apt['latitude'], apt['longitude'],
                apt['contact_info'], apt['lowest_price'], apt['times_contacted'],
                apt['last_updated'], apt['phone_number'], apt['notes'],
                apt['rating'], apt['is_tracked']
            ))

if __name__ == '__main__':
    populate_database()
    print("Database populated with sample data!")