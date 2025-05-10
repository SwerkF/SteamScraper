from flask import Flask, jsonify
from flask_cors import CORS
import csv
from db import db
app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/games")
def get_games():
    return jsonify({
        "data": {
            "games": [
                {
                    "name": "Game 1",
                    "price": 100,
                    "rating": 4.5
                }
            ]
        },
        "status": 200,
        "message": "Games fetched successfully"
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

    return jsonify({
        "data": {
            "cpu": list(cpus),
            "gpu": list(gpus),
            "memory": list(memory),
            "os": list(os)
        },
        "status": 200,
        "message": "Filters fetched successfully"
    })


if __name__ == "__main__":
    app.run(debug=True)

