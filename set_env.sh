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

# Path to secrets
sheets_creds_path="/home/juaneshberger/Credentials/spx_sheets.toml"

# Load sheet URLs
info_gdrive=$(cat $sheets_creds_path | grep info_gdrive | cut -d"'" -f2)
prices_gdrive=$(cat $sheets_creds_path | grep prices_gdrive | cut -d"'" -f2)
financials_gdrive=$(cat $sheets_creds_path | grep financials_gdrive | cut -d"'" -f2)

# Set environment variables
export SPX_INFO_GDRIVE=$info_gdrive
export SPX_PRICES_GDRIVE=$prices_gdrive
export SPX_FINANCIALS_GDRIVE=$financials_gdrive
