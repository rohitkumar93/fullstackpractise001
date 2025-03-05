#!/bin/bash
set -e

echo "Running entrypoint..."

# Function to check if PostgreSQL is ready
function wait_for_postgres() {
  until pg_isready -h postgres_service -p 5432 -U "$POSTGRES_USER"; do
    echo "Waiting for PostgreSQL to be ready..."
    sleep 2
  done
}

# Check if the database exists
echo "Checking if the database exists..."
DB_EXISTS=$(psql -U "$POSTGRES_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'")

# Create the database if it doesn't exist
if [ "$DB_EXISTS" != "1" ]; then
  echo "Database does not exist. Creating database and installing pgvector extension..."
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
      CREATE DATABASE $POSTGRES_DB;
      \c $POSTGRES_DB
      CREATE EXTENSION IF NOT EXISTS vector;
  EOSQL
else
  echo "Database already exists."
fi

# Wait for PostgreSQL to be ready
wait_for_postgres

# Run Alembic migrations
echo "Running Alembic migrations..."
alembic upgrade head || {
  echo "Alembic migrations failed. Exiting."
  exit 1
}

# Start the PostgreSQL server in the background
echo "Starting PostgreSQL server..."
postgres &

# Start the FastAPI application
echo "Starting FastAPI application..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
