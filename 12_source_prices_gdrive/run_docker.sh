#!/bin/bash

# Load the Google Cloud credentials
export JSON_CREDS=$(jq -c . < ~/Credentials/gdrive_credentials.json)

# Set Google Sheets credentials
sheets_creds_path="/home/juaneshberger/Credentials/spx_sheets.toml"
info_gdrive=$(cat $sheets_creds_path | grep info_gdrive | cut -d"'" -f2)
prices_gdrive=$(cat $sheets_creds_path | grep prices_gdrive | cut -d"'" -f2)
financials_gdrive=$(cat $sheets_creds_path | grep financials_gdrive | cut -d"'" -f2)
export SPX_INFO_GDRIVE=$info_gdrive
export SPX_PRICES_GDRIVE=$prices_gdrive
export SPX_FINANCIALS_GDRIVE=$financials_gdrive

# Run the Docker container with the environment variables
docker run -e JSON_CREDS="$JSON_CREDS" -e SPX_INFO_GDRIVE="$SPX_INFO_GDRIVE" -e SPX_PRICES_GDRIVE="$SPX_PRICES_GDRIVE" -e SPX_FINANCIALS_GDRIVE="$SPX_FINANCIALS_GDRIVE" spx_12_source_prices_gdrive
