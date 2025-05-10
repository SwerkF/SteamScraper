#!/bin/bash
set -e

# MongoDB connection parameters
MONGO_HOST="mongodb"
MONGO_PORT="27017"
MONGO_USER="admin"
MONGO_PASSWORD="password"
DB_NAME="steam_games"

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to start..."
until mongosh --host $MONGO_HOST --port $MONGO_PORT --username $MONGO_USER --password $MONGO_PASSWORD --eval "print('MongoDB connection successful')" > /dev/null 2>&1; do
  echo "MongoDB is unavailable - sleeping"
  sleep 1
done

echo "MongoDB is up - initializing database..."

# Create database and collections
mongosh --host $MONGO_HOST --port $MONGO_PORT --username $MONGO_USER --password $MONGO_PASSWORD <<EOF
use $DB_NAME

db.createCollection("games")
db.createCollection("gpu")
db.createCollection("cpu")
db.createCollection("memory")
db.createCollection("storage")
db.createCollection("os")

print("Database initialized with sample data!");
EOF

echo "Initialization completed!"
