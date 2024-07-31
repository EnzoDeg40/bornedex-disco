from flask import Flask, request, render_template, jsonify, send_file

import base64
import os
import random
import string
from io import BytesIO

import db
import img
import models.borne as borne

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')

global thedb

thedb = db.Database()
theimg = img.Image()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bornes/<image_id>.jpg', methods=['GET'])
def get_image(image_id):
    id = image_id
    if id is None:
        return jsonify({'error': 'No ID provided'}), 400
    borne = thedb.get_borne_id(id)
    if borne is None:
        return jsonify({'error': 'Borne not found'}), 404
    image_data = borne['image']
    if image_data is None:
        return jsonify({'error': 'No image data found'}), 404
    return send_file(BytesIO(theimg.format_base64(image_data)), mimetype='image/jpeg')

@app.route('/debug')
def debug():
    return render_template('debug.html', bornes=thedb.get_bornes())

@app.route('/api/bornes/<id>', methods=['POST'])
def update_borne(id):
    rf = request.form

    if id is None:
        return jsonify({'error': 'No ID provided'}), 400

    borne = thedb.get_borne_id(id)
    if borne is None:
        return jsonify({'error': 'Borne not found'}), 404

    if rf.get('name') is not None:
        borne['name'] = rf.get('name')
    if rf.get('is_valid') is not None:
        borne['is_valid'] = rf.get('is_valid')
    if rf.get('lat') is not None:
        borne['lat'] = rf.get('lat')
    if rf.get('lon') is not None:
        borne['lon'] = rf.get('lon')
    if rf.get('city') is not None:
        borne['city'] = rf.get('city')
    if rf.get('alt') is not None:
        borne['alt'] = rf.get('alt')
    if rf.get('is_valid') is not None:
        borne['is_valid'] = rf.get('is_valid')
    # thedb.update_borne(borne)
    thedb.update_new_borne(borne)
    return jsonify({'success': True})

@app.route('/upload', methods=['POST'])
def upload():
    rf = request.form

    image_data = rf.get('photo')
    if image_data is None:
        return jsonify({'error': 'No image data provided'}), 400
    
    myborne = borne.Borne(rf.get('name'), rf.get('lat'), rf.get('lon'), rf.get('city'))
    if not myborne.is_valid_data():
        return jsonify({'error': 'Invalid Borne data'}), 400
    
    if not myborne.set_image(image_data):
        return jsonify({'error': 'Failed to set image'}), 400
    
    if not thedb.add_borne(myborne):
        return jsonify({'error': 'Failed to add Borne to database'}), 500

    return jsonify({'success': True})

@app.route('/bornes', methods=['GET'])
def get_bornes():
    bornes = thedb.get_bornes()
    return jsonify(bornes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
