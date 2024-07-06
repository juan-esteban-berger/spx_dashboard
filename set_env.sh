#!/bin/bash

# Path to secrets
pg_creds_path="/home/juaneshberger/Credentials/pgcreds.json"

# Load database credentials    
host=$(jq -r '.host' $pg_creds_path)
port=$(jq -r '.port' $pg_creds_path)
user=$(jq -r '.user' $pg_creds_path)
password=$(jq -r '.password' $pg_creds_path)
database=$(jq -r '.database' $pg_creds_path)

# Set environment variables
export HOST=$host
export PORT=$port
export USER=$user
export PGPASSWORD=$password
export DATABASE=$database

# Set Google Cloud credentials
export JSON_CREDS=$(jq -c . ~/Credentials/gdrive_credentials.json)
