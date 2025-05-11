import os
import json
from pymongo import MongoClient

# Connexion MongoDB
client = MongoClient("mongodb://localhost:27017")  # adapte si besoin

# Base et chemin des fichiers
db = client["steam_etl"]
data_folder = "etl_pipeline/data"

# Mapping fichiers -> collections
file_to_collection = {
    "games_data.json": "games_metadata",
    "steam_store_links.json": "store_links",
    "steam_min_sysreqs_all_os.json": "system_requirements"
}

# Chargement des fichiers JSON
for filename, collection_name in file_to_collection.items():
    file_path = os.path.join(data_folder, filename)

    if not os.path.exists(file_path):
        print(f"⛔ Fichier introuvable : {file_path}")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

        # Cas dictionnaire : on transforme en liste de documents
        if isinstance(data, dict):
            data = [
                {"game_name": k, **v} if isinstance(v, dict) else {"game_name": k, "value": v}
                for k, v in data.items()
            ]

        if isinstance(data, list):
            db[collection_name].delete_many({})  # Nettoyage de la collection
            db[collection_name].insert_many(data)
            print(f"✅ {filename} ➔ collection '{collection_name}' (✓ {len(data)} documents)")
        else:
            print(f"⚠️ Format inattendu dans {filename}, sauté.")

print("\n📁 Insertion terminée.")
