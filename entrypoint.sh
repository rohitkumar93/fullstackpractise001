#!/bin/bash
set -e

# Check if the database exists
DB_EXISTS=$(psql -U "$POSTGRES_USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='$POSTGRES_DB'")

# Create the database if it doesn't exist
if [ "$DB_EXISTS" != "1" ]; then
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
      CREATE DATABASE $POSTGRES_DB;
      \c $POSTGRES_DB
      CREATE EXTENSION IF NOT EXISTS vector;
  EOSQL
fi

# Start the PostgreSQL server
exec postgres