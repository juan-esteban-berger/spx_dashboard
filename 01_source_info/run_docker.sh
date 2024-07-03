#!/bin/bash

# Path to secrets
pg_creds_path="pgcreds.json"

# Load database credentials    
host=$(jq -r '.host' $pg_creds_path)
port=$(jq -r '.port' $pg_creds_path)
user=$(jq -r '.user' $pg_creds_path)
password=$(jq -r '.password' $pg_creds_path)
database=$(jq -r '.database' $pg_creds_path)

# Run docker image with environment variables
docker run -e HOST=$host -e PORT=$port -e USER=$user -e PGPASSWORD=$password -e DATABASE=$database --network host spx_01_source_info
