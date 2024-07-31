import pymongo
from bson import ObjectId
from dotenv import load_dotenv
import os

import models.borne as borne

load_dotenv()

if os.environ.get('MONGODB_URI') is None:
    raise Exception('MONGODB_URI environment variable is not set')

if os.environ.get('ENV') is None:
    raise Exception('ENV environment variable is not set (must be dev or prod)')

class Database:
    def __init__(self):
        try:
            self.client = pymongo.MongoClient(os.environ.get('MONGODB_URI'))
            self.client.admin.command('ping')
            if os.environ.get('ENV') == 'dev':
                self.db = self.client['bornes_db_dev']
            else:
                self.db = self.client['bornes_db']
            print('Connected to MongoDB')
        except pymongo.errors.ConnectionError as e:
            raise Exception(f'Failed to connect to MongoDB: {e}')

    def get_bornes(self):
        bornes_collection = self.db['bornes']
        bornes_list = list(bornes_collection.find())
        for borne in bornes_list:
            borne['_id'] = str(borne['_id'])
        return bornes_list
    
    def get_borne_id(self, id):
        bornes_collection = self.db['bornes']
        borne = bornes_collection.find_one({'_id': ObjectId(id)})  # Use bson.ObjectId
        if borne is not None:
            borne['_id'] = str(borne['_id'])
        return borne

    def add_borne(self, borne):
        bornes_collection = self.db['bornes']
        borne_data = {
            'name': borne.name,
            'lat': borne.lat,
            'lon': borne.lon,
            'city': borne.city,
            'image': borne.image,
            'is_valid': False,
        }
        bornes_collection.insert_one(borne_data)
        return True