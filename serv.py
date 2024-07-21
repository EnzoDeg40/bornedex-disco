from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    print('Request:', request.form.image_data)
    
    # image_data = request.form.get('image_data')
    # lat = request.form.get('lat')
    # lon = request.form.get('lon')
    
    # # Process the image data, latitude, and longitude here
    # print('Image data:', image_data)
    # print('Latitude:', lat)
    # print('Longitude:', lon)
    
    return 'Upload successful'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
