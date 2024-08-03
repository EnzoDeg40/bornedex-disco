import base64
import os

class Image:
    def __init__(self):
        pass

    def format_base64(self, image_data):
        if image_data.startswith("data:image"):
            image_data = image_data.split(",")[1]
        
        missing_padding = len(image_data) % 4
        if missing_padding != 0:
            image_data += "=" * (4 - missing_padding)

        return base64.b64decode(image_data)
    
    def save_base64_image(self, image_data, file_path):
        img = Image.format_base64(image_data)
        with open(file_path, "wb") as file:
            file.write(img)






# Image.save_base64_image(base64_image, 'image.jpg')