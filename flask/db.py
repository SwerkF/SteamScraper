from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:password@localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "steam_games")

client = MongoClient(MONGO_URI)

db = client[DB_NAME]

games = db.games
cpus = db.cpus
gpus = db.gpus
memory = db.memory
os = db.os
games_requirements = db.games_requirements

def get_database():
    return db

def test_connection():
    try:
        client.admin.command('ismaster')
        print("MongoDB connection successful")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
