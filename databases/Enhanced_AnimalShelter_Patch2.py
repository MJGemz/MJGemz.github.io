from pymongo import MongoClient
from bson.objectid import ObjectId


class AnimalShelter:
    """
    Database-enhanced CRUD system for MongoDB Animal collection.
    Patch 2 focuses on advanced database operations such as:
    filtering, projections, sorting, counting, and safer ObjectId handling.
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
    # DATABASE CONNECTION
    # ----------------------------
    def connect_db(self):
        try:
            uri = f"mongodb://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}"
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.database = self.client[self.DB]
            self.collection = self.database[self.COL]

            self.client.server_info()
            print("Database connection successful.")

        except Exception as e:
            print(f"Database connection failed: {e}")
            self.client = None

    # ----------------------------
    # VALIDATION
    # ----------------------------
    def validate_data(self, data):
        if data is None:
            return False
        if not isinstance(data, dict):
            return False
        if len(data) == 0:
            return False
        return True

    # ----------------------------
    # CREATE
    # ----------------------------
    def create(self, data):
        if not self.validate_data(data):
            print("Invalid data provided. Insert failed.")
            return False

        try:
            result = self.collection.insert_one(data)
            return result.inserted_id is not None

        except Exception as e:
            print(f"Insert failed: {e}")
            return False

    # ----------------------------
    # READ (basic)
    # ----------------------------
    def read(self, query=None):
        try:
            if query is None:
                query = {}
            return list(self.collection.find(query))

        except Exception as e:
            print(f"Read failed: {e}")
            return []

    # =========================================================
    # PATCH 2: DATABASE ENHANCEMENTS
    # =========================================================

    # ----------------------------
    # READ BY FIELD (dynamic query)
    # ----------------------------
    def read_by_field(self, field, value):
        """Search using any field dynamically."""
        try:
            query = {field: value}
            return list(self.collection.find(query))

        except Exception as e:
            print(f"Read by field failed: {e}")
            return []

    # ----------------------------
    # READ WITH PROJECTION
    # ----------------------------
    def read_selected_fields(self, query=None, fields=None):
        """
        Return only selected fields (projection).
        Example fields: {"breed": 1, "name": 1}
        """
        try:
            if query is None:
                query = {}
            if fields is None:
                fields = {}

            return list(self.collection.find(query, fields))

        except Exception as e:
            print(f"Projection read failed: {e}")
            return []

    # ----------------------------
    # SORTED READ
    # ----------------------------
    def read_sorted(self, query=None, sort_field="breed"):
        """Return sorted results by a field."""
        try:
            if query is None:
                query = {}

            return list(self.collection.find(query).sort(sort_field, 1))

        except Exception as e:
            print(f"Sorted read failed: {e}")
            return []

    # ----------------------------
    # COUNT RECORDS
    # ----------------------------
    def count_records(self, query=None):
        """Count documents in collection."""
        try:
            if query is None:
                query = {}

            return self.collection.count_documents(query)

        except Exception as e:
            print(f"Count failed: {e}")
            return 0

    # ----------------------------
    # SAFE OBJECT ID HANDLING
    # ----------------------------
    def safe_object_id(self, id_value):
        """Validate ObjectId before using it in queries."""
        if ObjectId.is_valid(id_value):
            return ObjectId(id_value)
        return None

    # ----------------------------
    # UPDATE (safe enhancement version)
    # ----------------------------
    def update_one_record(self, query, new_values):
        """Update a single record safely."""
        if not self.validate_data(new_values):
            print("Invalid update data.")
            return False

        try:
            result = self.collection.update_one(query, {"$set": new_values})
            return result.modified_count > 0

        except Exception as e:
            print(f"Update failed: {e}")
            return False

    # ----------------------------
    # DELETE (safe enhancement version)
    # ----------------------------
    def delete_one_record(self, query):
        """Delete a single record safely."""
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count > 0

        except Exception as e:
            print(f"Delete failed: {e}")
            return False
