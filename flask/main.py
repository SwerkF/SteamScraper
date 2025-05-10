from flask import Flask, jsonify
from flask_cors import CORS
import csv

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
    return jsonify({
        "data": {
            "cpu": [
                {
                    "id": 1,
                    "name": "Intel Core i5-12600K"
                },
                {
                    "id": 2,
                    "name": "Intel Core i5-12600K"
                }
            ],
            "gpu": [
                {
                    "id": 1,
                    "name": "NVIDIA GeForce RTX 3060"
                },

            ],
            "memory": [
                {
                    "id": 1,
                    "name": "16GB DDR4"
                },
                {
                    "id": 2,
                    "name": "32GB DDR4"
                }
            ],
            "os": [
                {
                    "id": 1,
                    "name": "Windows 10"
                },
                {
                    "id": 2,
                    "name": "Windows 11"
                },
                {
                    "id": 3,
                    "name": "Linux"
                }
            ]
        },
        "status": 200,
        "message": "Filters fetched successfully"
    })

if __name__ == "__main__":
    app.run(debug=True)

