#!/bin/bash

# Path to secrets
pgsql_creds_path="/home/juaneshberger/Credentials/pgcreds.json"

# Load database credentials
creds=$(jq -r '. | to_entries | map("\(.key)=\(.value|tostring)") | .[]' $pgsql_creds_path)

# Create Kubernetes secrets
for cred in $creds
do
  key=$(echo $cred | cut -f1 -d'=')
  value=$(echo $cred | cut -f2 -d'=' | tr -d '\r\n')

  kubectl delete secret spx-streamlit-$key --ignore-not-found
  echo -n $value | kubectl create secret generic spx-streamlit-$key --from-file=$key=/dev/stdin

done
sleep 3
kubectl get secrets
