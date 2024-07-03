#!/bin/bash

# Path to secrets
msql_creds_path="/home/juaneshberger/Credentials/mssql_creds_k8s.json"

# Load database credentials
creds=$(jq -r ". | to_entries| .[] | .key + \"=\" + .value" $msql_creds_path)

# Create Kubernetes secrets
for cred in $creds
do
  key=$(echo $cred | cut -f1 -d'=')
  value=$(echo $cred | cut -f2 -d'=') 
  echo $value > tmp.txt
  microk8s kubectl delete secret spx-streamlit-$key
  microk8s kubectl create secret generic spx-streamlit-$key --from-file=$key=tmp.txt
  rm tmp.txt
done
sleep 3
kubectl get secrets
