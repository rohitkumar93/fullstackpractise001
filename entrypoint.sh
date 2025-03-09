#!/bin/bash

# Wait for PostgreSQL to be ready
# echo "Waiting for PostgreSQL..."
# while ! pg_isready -h localhost -p 5432 -U postgres; do
#   sleep 1
# done

# echo "PostgreSQL is ready!"

# Install the pgvector extension (if not exists) (Update: Now being handled by init.sql)
# echo "Creating pgvector extension..."
# psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Apply Alembic migrations
# echo "Running Alembic migrations..."
# alembic upgrade head (Update: Now being handled by docker-compose)

# Start FastAPI
# echo "Starting FastAPI application..."
# exec uvicorn app.main:app --host 0.0.0.0 --port 8000
