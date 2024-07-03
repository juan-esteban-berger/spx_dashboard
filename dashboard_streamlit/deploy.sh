# Delete the old docker image
sudo docker rmi juanestebanberger/spx_streamlit:latest

# Build the docker image
sudo docker build -t juanestebanberger/spx_streamlit:latest .

# Push the docker image to the docker hub
sudo docker push juanestebanberger/spx_streamlit:latest

# Delete the old deployment
microk8s kubectl delete deployment spx-streamlit-deployment

# Delete the old service
microk8s kubectl delete service spx-streamlit-service

# Apply the Kubernetes deployment
microk8s kubectl apply -f deployment.yaml

# Apply the Kubernetes service
microk8s kubectl apply -f service.yaml

# Get SVC
microk8s kubectl get svc
