from flask import Flask, request, render_template, jsonify

import base64
import os
import random
import string
from PIL import Image
from io import BytesIO
import sqlite3

import init
import db

import models.borne as borne

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')

global thedb

thedb = db.Database()

@app.route('/')
def index():
    return render_template('index.html')

def save_base64_image(base64_string, output_dir, filename=None):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
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
        return jsonify({'error': 'No image data provided'}), 400
    
    myborne = borne.Borne(rf.get('name'), rf.get('lat'), rf.get('lon'), rf.get('city'))
    if not myborne.is_valid():
        return jsonify({'error': 'Invalid Borne data'}), 400
    
    if not thedb.add_borne(myborne):
        return jsonify({'error': 'Failed to add Borne to database'}), 500

    return jsonify({'error': 'Failed to save image'}), 500

    # if not save_base64_image(image_data, 'images', str(borne_id) + '.png'):
    #     return (jsonify({'error': 'Failed to save image'}), 500)


    return jsonify({'success': True})

@app.route('/bornes', methods=['GET'])
def get_bornes():
    bornes = thedb.get_bornes()
    return jsonify(bornes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
