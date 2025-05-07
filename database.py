# database.py
from pymongo import MongoClient
from config import MONGO_URI, OWNER_ID

client = MongoClient(MONGO_URI)
db = client["AutoIndex"]

files = db["files"]
users = db["users"]
admins = db["admins"]

# Add file info (used for indexing documents)
async def add_file(file_name, message_id, file_size):
    files.update_one(
        {"message_id": message_id},
        {"$set": {
            "file_name": file_name,
            "file_size": file_size,
            "message_id": message_id
        }},
        upsert=True
    )

# Search files using case-insensitive regex
def search_files(query):
    return files.find({"file_name": {"$regex": query, "$options": "i"}})

# Register a new user (used in /start)
async def add_user(user_id):
    users.update_one({"_id": user_id}, {"$setOnInsert": {"banned": False}}, upsert=True)

# Ban a user
async def ban_user(user_id):
    users.update_one({"_id": user_id}, {"$set": {"banned": True}})

# Unban a user
async def unban_user(user_id):
    users.update_one({"_id": user_id}, {"$set": {"banned": False}})

# Check if user is banned
async def is_banned(user_id):
    user = users.find_one({"_id": user_id})
    return user.get("banned", False) if user else False

# Check if a user is an admin
def is_admin(user_id):
    return user_id == OWNER_ID or admins.find_one({"_id": user_id}) is not None

# Add an admin
def add_admin(user_id):
    admins.update_one({"_id": user_id}, {"$setOnInsert": {}}, upsert=True)

# Remove an admin
def remove_admin(user_id):
    admins.delete_one({"_id": user_id})

# Get overall bot statistics
def get_stats():
    return {
        "files": files.count_documents({}),
        "users": users.count_documents({}),
        "admins": admins.count_documents({})
    }
