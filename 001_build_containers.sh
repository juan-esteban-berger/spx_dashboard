#!/bin/bash

# Array of container names
containers=(
    "spx_01_source_info"
    "spx_02_source_prices"
    "spx_03_source_financials"
    "spx_11_source_info_gdrive"
    "spx_12_source_prices_gdrive"
    "spx_13_source_financials_gdrive"
)

# Function to build a Docker container
build_container() {
    local container_name=$1
    local directory=${container_name#spx_}

    echo "Building $container_name..."
    cd "$directory" || exit
    
    # Remove existing container and image
    docker rm -f "$container_name" 2>/dev/null
    docker rmi -f "$container_name" 2>/dev/null
    
    # Build new container
    docker build -t "$container_name" .
    
    cd ..
    echo "Finished building $container_name"
    echo
}

# Main script execution
echo "Starting to build Docker containers..."
echo

for container in "${containers[@]}"; do
    build_container "$container"
done

echo "All containers have been rebuilt successfully!"
