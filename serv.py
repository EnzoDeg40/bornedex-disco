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
    def __init__(self, lat, lon, city):
        self.id = None
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

def save_base64_image(base64_string, output_dir):
    # Extraire la partie base64 de la chaîne
    base64_data = base64_string.split(',')[1]
    
    # Décoder la chaîne base64
    image_data = base64.b64decode(base64_data)
    
    # Créer une image à partir des données décodées
    image = Image.open(BytesIO(image_data))
    
    # Générer un nom de fichier aléatoire
    random_filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + '.png'
    
    # Créer le chemin complet pour l'image
    output_path = os.path.join(output_dir, random_filename)
    
    # Sauvegarder l'image
    image.save(output_path)
    
    return output_path

@app.route('/upload', methods=['POST'])
def upload():
    
    image_data = request.form.get('photo')
    if image_data is None:
        return 'No image data'   
    
    borne = Borne(request.form.get('lat'), request.form.get('lon'), request.form.get('city'))
    if not borne.is_valid():
        return (jsonify({'error': 'Invalid Borne data'}), 400)
    
    # Save the image
    image_path = save_base64_image(image_data, 'images')

    # Connect to SQLite database
    conn = sqlite3.connect('bornes.db')
    cursor = conn.cursor()

    # Insert Borne data into the database
    cursor.execute("INSERT INTO bornes (nom, lon, lat, ville, is_valid) VALUES (?, ?, ?, ?, ?)", (image_path, borne.lon, borne.lat, borne.city, 0))
    conn.commit()

    # Close the database connection
    conn.close()


    # Return a success response
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
