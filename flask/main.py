from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
from db import db
from bson import ObjectId

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/games")
def get_games():
    filters = request.args

    cpu_name = filters.get("cpu")
    gpu_name = filters.get("gpu")
    memory_name = filters.get("memory")
    os_name = filters.get("os")
    pricehigh = int(filters.get("pricehigh", 100))
    pricelow = int(filters.get("pricelow", 0))
    search = filters.get("search", "")
    page = int(filters.get("page", 1))

    pipeline = []
    match_conditions = {}


    # Filtrage par texte
    if search:
        match_conditions["name"] = {"$regex": search, "$options": "i"}

    # Filtrage par prix
    if pricelow or pricehigh < 100:
        price_condition = {}
        if pricelow:
            price_condition["$gte"] = pricelow
        if pricehigh < 100:
            price_condition["$lte"] = pricehigh
        if price_condition:
            match_conditions["$or"] = [
                {"price": price_condition},
            ]

    # Logique pour le filtrage CPU
    if cpu_name:
        cpu = db.cpu.find_one({"name": cpu_name})
        if cpu:
            cpu_rank = cpu.get("rank")
            if cpu_rank:
                # Trouver les CPU de même rang ou inférieur
                lower_ranked_cpus = list(db.cpu.find({"rank": {"$gte": cpu_rank}}, {"_id": 1}))
                lower_ranked_cpu_ids = [cpu["_id"] for cpu in lower_ranked_cpus]

                # Inclure les jeux qui ont un CPU référencé ou "any" dans les modèles
                pipeline.append({
                    "$match": {
                        "$or": [
                            {"system_requirements.win.cpu.models": "any"},
                            {"system_requirements.mac.cpu.models": "any"},
                            {"system_requirements.linux.cpu.models": "any"},
                            {"system_requirements.win.cpu.refs": {"$in": lower_ranked_cpu_ids}},
                            {"system_requirements.mac.cpu.refs": {"$in": lower_ranked_cpu_ids}},
                            {"system_requirements.linux.cpu.refs": {"$in": lower_ranked_cpu_ids}}
                        ]
                    }
                })

    # Logique pour le filtrage GPU
    if gpu_name:
        gpu = db.gpu.find_one({"name": gpu_name})
        if gpu:
            gpu_rank = gpu.get("rank")
            if gpu_rank:
                # Trouver les GPU de même rang ou inférieur
                lower_ranked_gpus = list(db.gpu.find({"rank": {"$gte": gpu_rank}}, {"_id": 1}))
                lower_ranked_gpu_ids = [gpu["_id"] for gpu in lower_ranked_gpus]

                # Inclure les jeux qui ont un GPU référencé ou "any" dans les modèles
                pipeline.append({
                    "$match": {
                        "$or": [
                            {"system_requirements.win.gpu.models": "any"},
                            {"system_requirements.mac.gpu.models": "any"},
                            {"system_requirements.linux.gpu.models": "any"},
                            {"system_requirements.win.gpu.refs": {"$in": lower_ranked_gpu_ids}},
                            {"system_requirements.mac.gpu.refs": {"$in": lower_ranked_gpu_ids}},
                            {"system_requirements.linux.gpu.refs": {"$in": lower_ranked_gpu_ids}}
                        ]
                    }
                })

    # Logique pour le filtrage RAM
    if memory_name:
        # Extraire la valeur numérique de la RAM (ex: "8GB RAM" -> 8)
        import re
        ram_value_match = re.search(r'(\d+)', memory_name)
        if ram_value_match:
            ram_value = int(ram_value_match.group(1))

            valid_ram_ids = []
            all_ram = list(db.memory.find({}))

            for ram_doc in all_ram:
                ram_name = ram_doc.get("name", "")
                ram_match = re.search(r'(\d+)', ram_name)

                if ram_match:
                    current_ram_value = int(ram_match.group(1))
                    if current_ram_value <= ram_value:
                        valid_ram_ids.append(ram_doc["_id"])

            if valid_ram_ids:
                pipeline.append({
                    "$match": {
                        "$or": [
                            {"system_requirements.win.ram.refs": {"$in": valid_ram_ids}},
                            {"system_requirements.mac.ram.refs": {"$in": valid_ram_ids}},
                            {"system_requirements.linux.ram.refs": {"$in": valid_ram_ids}}
                        ]
                    }
                })

    # Filtrage par OS
    if os_name:
        windows_compatibility = {
            "Windows 7": ["Windows 7"],
            "Windows 8": ["Windows 7", "Windows 8"],
            "Windows 10": ["Windows 7", "Windows 8", "Windows 10"],
            "Windows 11": ["Windows 7", "Windows 8", "Windows 10", "Windows 11"]
        }

        compatible_os = []
        if os_name in windows_compatibility:
            compatible_versions = windows_compatibility[os_name]
            compatible_os = list(db.os.find({"name": {"$in": compatible_versions}}, {"_id": 1}))
            os_ids = [os["_id"] for os in compatible_os]

            pipeline.append({
                "$match": {
                    "system_requirements.win.os.refs": {"$in": os_ids}
                }
            })
        else:
            os = db.os.find_one({"name": os_name})
            if os:
                os_id = os["_id"]
                pipeline.append({
                    "$match": {
                        "$or": [
                            {"system_requirements.mac.os.refs": os_id},
                            {"system_requirements.linux.os.refs": os_id}
                        ]
                    }
                })

    # Pagination
    skip = (page - 1) * 9

    # Ajout des conditions de correspondance
    if match_conditions:
        pipeline.append({"$match": match_conditions})

    # Projection pour retourner seulement les champs nécessaires
    pipeline.append({
        "$project": {
            "_id": 0,
            "name": 1,
            "price": 1,
            "rating": 1,
            "developer": 1,
            "release_date": 1,
            "publisher": 1,
            "supported_systems": 1,
            "store_url": 1,
            "image_url": 1,
            "app_id": 1
        }
    })

    # Ajout de skip et limit
    pipeline.append({"$skip": skip})
    pipeline.append({"$limit": 9})

    # Exécution du pipeline
    if pipeline:
        games = list(db.games.aggregate(pipeline))
    else:
        games = list(db.games.find({}, {
            "_id": 0,
            "name": 1,
            "price": 1,
            "rating": 1,
            "developer": 1,
            "supported_systems": 1,
            "store_url": 1,
            "image_url": 1,
            "app_id": 1
        }).skip(skip).limit(9))

    count_pipeline = pipeline[:-2] if pipeline else []
    count = len(list(db.games.aggregate(count_pipeline))) if pipeline else db.games.count_documents({})

    return jsonify({
        "data": games,
        "status": 200,
        "message": "Games fetched successfully",
        "count": count
    })

@app.route("/api/filters")
def get_filters():

    cpus = db.cpu.find(
        {}, {"_id": 0, "name": 1, "id": 1, "rank": 1}
    ).sort("rank", 1)
    gpus = db.gpu.find(
        {}, {"_id": 0, "name": 1, "id": 1, "rank": 1}
    ).sort("rank", 1)
    memory = db.memory.find(
    {}, {"_id": 0, "name": 1, "id": 1}
    )
    os = db.os.find(
    {}, {"_id": 0, "name": 1, "id": 1}
    )

    editors = db.games.distinct("developer")

    return jsonify({
        "data": {
            "cpu": list(cpus),
            "gpu": list(gpus),
            "memory": list(memory),
            "os": list(os),
            "editors": list(editors)
        },
        "status": 200,
        "message": "Filters fetched successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)

