import base64
from io import BytesIO
from PIL import Image

class Borne:
    def __init__(self, name, lat, lon, city):
        self.id = None
        self.name = name
        self.lat = lat
        self.lon = lon
        self.city = city
        self.image = None
        self.is_valid = False

    def set_image(self, image):
        self.image = image
        return True
        # try:
        #     image_data = base64.b64decode(image)
        #     img = Image.open(BytesIO(image_data))
        #     img.verify()
        #     self.image = img
        # except (ValueError, IOError, TypeError) as e:
        #     print(f"Error setting image: {e}")
        #     return False
        # return True
        try:
            base64_data = image.split(',')[1]
            image_data = base64.b64decode(base64_data)
            img = Image.open(BytesIO(image_data))
            img.verify()
            if len(image_data) > 10 * 1024 * 1024:
                print("Error: Image is too heavy.")
                return False

            self.image = img # this line is wrong ?
        except (ValueError, IOError, TypeError) as e:
            print(f"Error setting image: {e}")
            return False
    
    def is_valid_data(self):
        if self.lat is None or self.lon is None or self.city is None:
            return False
        try:
            float(self.lat)
            float(self.lon)
        except ValueError:
            return False
        return True