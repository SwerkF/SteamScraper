#!/bin/bash
set -e

sleep 5

mongosh --host localhost --port 27017 -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD --authenticationDatabase admin <<EOF
# Créer la base de données
use $MONGO_INITDB_DATABASE

echo "MongoDB is up - initializing database..."

db.createCollection("games")
db.createCollection("gpu")
db.createCollection("cpu")
db.createCollection("memory")
db.createCollection("storage")
db.createCollection("os")
db.createCollection("games_requirements")

# Insert memory data
db.memory.insertMany([
  {
    "id": 1,
    "name": "4GB RAM"
  },
  {
    "id": 2,
    "name": "8GB RAM"
  },
  {
    "id": 3,
    "name": "16GB RAM"
  },
  {
    "id": 4,
    "name": "32GB RAM"
  },
  {
    "id": 5,
    "name": "64GB RAM"
  }
])

# Insert OS data
db.os.insertMany([
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
  },
  {
    "id": 4,
    "name": "MacOS"
  }
])

print("Database initialized with sample data!");
EOF

echo "Initialization completed!"
