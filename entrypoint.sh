#!/bin/sh

set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Waiting for PostgreSQL to be ready..."



    # Check if PostgreSQL is running

#    ps -ef | grep postgres > /dev/null 2>&1
#
#    if [ $? -eq 0 ]; then
#
#        # Install pgvector extension
#
#        psql -c "CREATE EXTENSION IF NOT EXISTS pgvector;"
#
#    fi
#


echo "🔥 Starting FastAPI server..."

# Run Alembic migrations
echo "✅ Running Alembic migrations..."
alembic upgrade head || echo "⚠️ Alembic migration failed, but continuing..."

# Ingest sample documents (doesn't block execution)
echo "✅ Ingesting sample documents..."
python -m backend.ingestion_service.sample_ingest || echo "⚠️ Ingestion failed, but continuing..."


#exec uvicorn main:app --host 0.0.0.0 --port 8000
