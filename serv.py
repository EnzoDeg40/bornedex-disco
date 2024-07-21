from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

class Borne:
    def __init__(self, lat, lon, city):
        # self.id = id
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

@app.route('/upload', methods=['POST'])
def upload():
    
    image_data = request.form.get('photo')
    if image_data is None:
        return 'No image data'   
    
    borne = Borne(request.form.get('lat'), request.form.get('lon'), request.form.get('city'))
    if not borne.is_valid():
        return 'Invalid data'
    
    return 'Upload successful'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
