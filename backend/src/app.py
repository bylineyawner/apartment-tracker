from flask import Flask, jsonify, request
from flask_cors import CORS
from database import ApartmentDB
import traceback
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:3001"],
        "methods": ["GET", "POST", "OPTIONS"]
    }
})

db = ApartmentDB()

@app.route('/api/apartments/search', methods=['POST'])
def search_apartments():
    try:
        data = request.json
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM apartments")
            apartments = []
            search_lat = float(data['lat'])
            search_lon = float(data['lon'])
            radius = float(data.get('radius', 5))
            
            for row in cursor.fetchall():
                apt = {
                    'id': row[0],
                    'name': row[1],
                    'address': row[2],
                    'latitude': row[3],
                    'longitude': row[4],
                    'contact_info': row[5],
                    'lowestPrice': row[6],
                    'timesContacted': row[7],
                    'lastUpdated': row[8],
                    'phone_number': row[9],
                    'notes': row[10],
                    'rating': row[11],
                    'is_tracked': bool(row[12]) if row[12] is not None else False
                }
                apartments.append(apt)
            
            return jsonify(apartments)
    except Exception as e:
        print(f"Error in search_apartments: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/apartments', methods=['POST'])
def add_apartment():
    try:
        data = request.json
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO apartments (
                    name, address, latitude, longitude, contact_info,
                    lowest_price, times_contacted, last_updated,
                    phone_number, notes, rating, is_tracked
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['name'],
                data['address'],
                data['latitude'],
                data['longitude'],
                data['contact_info'],
                data['lowest_price'],
                0,  # times_contacted starts at 0
                datetime.now(),
                data['phone_number'],
                data.get('notes', ''),
                data.get('rating', 0),
                False  # is_tracked starts as False
            ))
            conn.commit()
            return jsonify({'id': cursor.lastrowid}), 201
    except Exception as e:
        print(f"Error in add_apartment: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/apartments/<int:apartment_id>', methods=['PUT'])
def update_apartment(apartment_id):
    try:
        data = request.json
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE apartments SET
                    name = ?,
                    address = ?,
                    latitude = ?,
                    longitude = ?,
                    contact_info = ?,
                    lowest_price = ?,
                    phone_number = ?,
                    notes = ?,
                    rating = ?,
                    is_tracked = ?
                WHERE id = ?
            """, (
                data['name'],
                data['address'],
                data['latitude'],
                data['longitude'],
                data['contact_info'],
                data['lowest_price'],
                data['phone_number'],
                data.get('notes', ''),
                data.get('rating', 0),
                data.get('is_tracked', False),
                apartment_id
            ))
            conn.commit()
            return jsonify({'success': True})
    except Exception as e:
        print(f"Error in update_apartment: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)