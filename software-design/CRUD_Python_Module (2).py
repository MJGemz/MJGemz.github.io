from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username=None, password=None, host='localhost', port=27017, db_name='aac', collection_name='animals'):
        # If username/password are provided, use them; otherwise use default
        self.USER = username if username else 'aacuser'
        self.PASS = password if password else 'Password123'
        self.HOST = host
        self.PORT = port
        self.DB = db_name
        self.COL = collection_name

        # Initialize MongoDB connection
        try:
            self.client = MongoClient(f'mongodb://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}')
            self.database = self.client[self.DB]
            self.collection = self.database[self.COL]
        except Exception as e:
            print("Error connecting to MongoDB:", e)

    # CREATE method
    def create(self, data):
        if data is not None:
            try:
                self.collection.insert_one(data)  # data should be a dictionary
                return True
            except Exception as e:
                print("Insert failed:", e)
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    # READ method
    def read(self, query):
        try:
            cursor = self.collection.find(query)
            return list(cursor)  # Return results as a list
        except Exception as e:
            print("Read failed:", e)
            return []