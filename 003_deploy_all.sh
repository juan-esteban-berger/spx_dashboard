#!/bin/bash

# Change to the spx_dashboard directory
cd ~/spx_dashboard

# Run the secrets generation script
./dashboard_streamlit/kubectl_secrets.sh

# Deploy dashboard_streamlit
cd dashboard_streamlit
./deploy.sh
cd ..

# Deploy dashboard_tableau  
cd dashboard_tableau
./deploy.sh
cd ..

echo "Deployment complete!"
