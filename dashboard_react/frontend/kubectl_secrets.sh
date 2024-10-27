#!/bin/bash
# API URL - Frontend Settings
api_url_path="/home/juaneshberger/Credentials/spx-django.txt"
# API token path
api_token_path="/home/juaneshberger/Credentials/spx-django-token.txt"

# Create API URL secret
api_url=$(cat $api_url_path)
microk8s kubectl delete secret spx-react-api-url --ignore-not-found
echo -n $api_url | microk8s kubectl create secret generic spx-react-api-url --from-literal=url=$api_url

# Create API token secret
api_token=$(cat $api_token_path)
microk8s kubectl delete secret spx-react-api-token --ignore-not-found
echo -n $api_token | microk8s kubectl create secret generic spx-react-api-token --from-literal=token=$api_token

sleep 3
microk8s kubectl get secrets
