from flask import Flask, request, render_template, jsonify

import base64
import os
import random
import string
from PIL import Image
from io import BytesIO
import sqlite3

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

class Borne:
    def __init__(self, name, lat, lon, city):
        self.id = None
        self.name = name
        self.lat = lat
        self.lon = lon
        self.city = city
    
    def is_valid(self):
        if self.lat is None or self.lon is None or self.city is None:
            return False
        try:
            float(self.lat)
            float(self.lon)
        except ValueError:
            return False
        return True

def save_base64_image(base64_string, output_dir, filename=None):
    base64_data = base64_string.split(',')[1]
    image_data = base64.b64decode(base64_data)
    image = Image.open(BytesIO(image_data))
    
    if filename is None:
        filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.png'
    
    output_path = os.path.join(output_dir, filename)
    image.save(output_path)
    
    return True

@app.route('/upload', methods=['POST'])
def upload():
    rf = request.form

    image_data = rf.get('photo')
    if image_data is None:
        return (jsonify({'error': 'No image data provided'}), 400) 
    
    borne = Borne(rf.get('name'), rf.get('lat'), rf.get('lon'), rf.get('city'))
    if not borne.is_valid():
        return (jsonify({'error': 'Invalid Borne data'}), 400)
    
    try:
        conn = sqlite3.connect('bornes.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bornes (nom, lon, lat, ville) VALUES (?, ?, ?, ?)", (borne.name, borne.lon, borne.lat, borne.city))
        borne_id = cursor.lastrowid
        conn.commit()
        conn.close()
    except sqlite3.Error:
        return (jsonify({'error': 'Failed to insert Borne data'}), 500)

    if not save_base64_image(image_data, 'images', str(borne_id) + '.png'):
        return (jsonify({'error': 'Failed to save image'}), 500)


    return jsonify({'success': True})

@app.route('/bornes', methods=['GET'])
def get_bornes():
    # Connect to SQLite database
    conn = sqlite3.connect('bornes.db')
    cursor = conn.cursor()
    # Retrieve all Borne data from the database
    cursor.execute("SELECT * FROM bornes")
    bornes = cursor.fetchall()
    # Close the database connection
    conn.close()
    # Return the list of bornes as JSON response
    return jsonify({'bornes': bornes})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
