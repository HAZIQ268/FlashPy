# models.py

from flask_login import UserMixin
from pymongo import MongoClient
from bson.objectid import ObjectId

# MongoDB connection
client = MongoClient("mongodb+srv://samrasadaqat:admin12345@backend1.k7uropq.mongodb.net/?appName=backend1")
db = client["flask_auth_db"]
users_collection = db["users"]

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data.get("_id"))
        self.username = user_data.get("username")
        self.password = user_data.get("password")  # hashed password

    @staticmethod
    def get_by_username(username):
        user_data = users_collection.find_one({"username": username})
        return User(user_data) if user_data else None

    @staticmethod
    def get_by_id(user_id):
        try:
            user_data = users_collection.find_one({"_id": ObjectId(user_id)})
            return User(user_data) if user_data else None
        except:
            return None

    @staticmethod
    def create(username, hashed_password):
        # Check if user already exists
        if users_collection.find_one({"username": username}):
            return None
        user_id = users_collection.insert_one({
            "username": username,
            "password": hashed_password
        }).inserted_id
        return User.get_by_id(user_id)
