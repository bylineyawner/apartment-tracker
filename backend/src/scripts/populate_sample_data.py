# backend/src/scripts/populate_sample_data.py
import sqlite3
from datetime import datetime

sample_data = [
    {
        'name': 'Sunny Heights',
        'address': '123 Main St, San Francisco, CA',
        'latitude': 37.7749,
        'longitude': -122.4194,
        'contact_info': 'John Manager',
        'lowest_price': 2500,
        'phone_number': '(415) 555-0123',
        'notes': 'Great views of the city'
    },
    {
        'name': 'Bay View Apartments',
        'address': '456 Market St, San Francisco, CA',
        'latitude': 37.7897,
        'longitude': -122.4000,
        'contact_info': 'Sarah Agent',
        'lowest_price': 3000,
        'phone_number': '(415) 555-0124',
        'notes': 'Near public transit'
    },
    # Add more sample apartments here
]

def populate_database():
    conn = sqlite3.connect('../apartments.db')
    cursor = conn.cursor()
    
    for apt in sample_data:
        cursor.execute("""
            INSERT INTO apartments (
                name, address, latitude, longitude, 
                contact_info, lowest_price, times_contacted,
                last_updated, phone_number, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            apt['name'], apt['address'], apt['latitude'], apt['longitude'],
            apt['contact_info'], apt['lowest_price'], 0,
            datetime.now(), apt['phone_number'], apt['notes']
        ))
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_database()