from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection details
MONGO_URI = os.getenv("MONGO_URI", "mongodb://admin:password@localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "steam_games")

# Create a MongoDB client
client = MongoClient(MONGO_URI)

# Get database
db = client[DB_NAME]

# Collections
games = db.games
users = db.users

def get_database():
    return db

# Test connection
def test_connection():
    try:
        # The ismaster command is cheap and does not require auth
        client.admin.command('ismaster')
        print("MongoDB connection successful")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
