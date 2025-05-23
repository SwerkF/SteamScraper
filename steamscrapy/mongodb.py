from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging

# Désactiver les logs verbeux de PyMongo
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("pymongo.connection").setLevel(logging.WARNING)
logging.getLogger("pymongo.command").setLevel(logging.WARNING)
logging.getLogger("pymongo.serverSelection").setLevel(logging.WARNING)

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://root:password@localhost:27017/")
DB_NAME = os.getenv("DB_NAME", "steam_games")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

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
