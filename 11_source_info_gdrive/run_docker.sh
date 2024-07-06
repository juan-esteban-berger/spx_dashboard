#!/bin/bash

# Load the JSON credentials from the environment
export JSON_CREDS=$(jq -c . < ~/Credentials/gdrive_credentials.json)

# Run the Docker container with the environment variable
docker run -e JSON_CREDS="$JSON_CREDS" spx_11_source_info_gdrive
