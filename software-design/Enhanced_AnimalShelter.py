from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter:
    """
    Enhanced CRUD operations for Animal collection in MongoDB.
    Improvements include better error handling, input validation,
    modular structure, and safer database operations.
    """

    def __init__(self, username=None, password=None, host='localhost', port=27017,
                 db_name='aac', collection_name='animals'):

        self.USER = username if username else 'aacuser'
        self.PASS = password if password else 'Password123'
        self.HOST = host
        self.PORT = port
        self.DB = db_name
        self.COL = collection_name

        self.client = None
        self.database = None
        self.collection = None

        self.connect_db()

    # ----------------------------
    # DATABASE CONNECTION METHOD
    # ----------------------------
    def connect_db(self):
        """Establish MongoDB connection with error handling."""
        try:
            uri = f"mongodb://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}"
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.database = self.client[self.DB]
            self.collection = self.database[self.COL]

            # Simple connection test
            self.client.server_info()

            print("Database connection successful.")

        except Exception as e:
            print(f"Database connection failed: {e}")
            self.client = None

    # ----------------------------
    # DATA VALIDATION METHOD
    # ----------------------------
    def validate_data(self, data):
        """Basic validation to ensure data is not empty and is a dictionary."""
        if data is None:
            return False
        if not isinstance(data, dict):
            return False
        if len(data) == 0:
            return False
        return True

    # ----------------------------
    # CREATE METHOD
    # ----------------------------
    def create(self, data):
        """Insert a new record into MongoDB."""
        if not self.validate_data(data):
            print("Invalid data provided. Insert failed.")
            return False

        try:
            result = self.collection.insert_one(data)

            if result.inserted_id:
                print(f"Record inserted successfully with ID: {result.inserted_id}")
                return True

        except Exception as e:
            print(f"Insert failed: {e}")

        return False

    # ----------------------------
    # READ METHOD
    # ----------------------------
    def read(self, query=None):
        """Retrieve records from MongoDB."""
        try:
            if query is None:
                query = {}

            results = list(self.collection.find(query))

            if len(results) == 0:
                print("No records found.")
            else:
                print(f"Retrieved {len(results)} record(s).")

            return results

        except Exception as e:
            print(f"Read failed: {e}")
            return []

    # ----------------------------
    # UPDATE METHOD (NEW)
    # ----------------------------
    def update(self, query, new_values):
        """Update existing records in MongoDB."""
        if not self.validate_data(new_values):
            print("Invalid update data.")
            return False

        try:
            result = self.collection.update_many(query, {"$set": new_values})

            print(f"Matched {result.matched_count} record(s).")
            print(f"Modified {result.modified_count} record(s).")

            return result.modified_count > 0

        except Exception as e:
            print(f"Update failed: {e}")
            return False

    # ----------------------------
    # DELETE METHOD (NEW)
    # ----------------------------
    def delete(self, query):
        """Delete records from MongoDB."""
        try:
            result = self.collection.delete_many(query)

            print(f"Deleted {result.deleted_count} record(s).")

            return result.deleted_count > 0

        except Exception as e:
            print(f"Delete failed: {e}")
            return False
