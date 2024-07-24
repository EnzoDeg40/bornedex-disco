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