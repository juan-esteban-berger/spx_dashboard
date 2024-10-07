#!/bin/bash
# Path to secrets
pgsql_creds_path="/home/juaneshberger/Credentials/pgcreds.json"

# Load database credentials
creds=$(jq -r 'to_entries[] | "\(.key)=\(.value)"' $pgsql_creds_path)

# Create Kubernetes secrets
for cred in $creds
do
  key=$(echo $cred | cut -f1 -d'=')
  value=$(echo $cred | cut -f2 -d'=' | tr -d '\r\n')
  
  # Map 'host' to 'server' for consistency with deployment.yaml
  if [ "$key" == "host" ]; then
    secret_name="spx-streamlit-host"
    secret_key="server"
  else
    secret_name="spx-streamlit-$key"
    secret_key=$key
  fi
  
  microk8s kubectl delete secret $secret_name --ignore-not-found
  echo -n $value | microk8s kubectl create secret generic $secret_name --from-literal=$secret_key=$value
done

sleep 3
microk8s kubectl get secrets
