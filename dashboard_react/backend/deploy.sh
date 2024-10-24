#!/bin/bash

# Create Kubernetes secrets
./kubectl_secrets.sh

# Delete the old docker image
docker rmi juanestebanberger/spx_django:latest

# Build the docker image
docker build -t juanestebanberger/spx_django:latest .

# Push the docker image to docker hub
docker push juanestebanberger/spx_django:latest

# Delete the old deployment
microk8s kubectl delete deployment spx-django-deployment

# Delete the old service
microk8s kubectl delete service spx-django-service

# Apply the Kubernetes deployment
microk8s kubectl apply -f deployment.yaml

# Apply the Kubernetes service
microk8s kubectl apply -f service.yaml

# Get SVC
microk8s kubectl get svc
