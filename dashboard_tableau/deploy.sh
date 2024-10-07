docker build -t juanestebanberger/spx-tableau:latest .

docker push juanestebanberger/spx-tableau:latest

microk8s kubectl delete deployment spx-tableau-deployment --ignore-not-found=true
microk8s kubectl apply -f deployment.yaml
microk8s kubectl delete service spx-tableau-service --ignore-not-found=true
microk8s kubectl apply -f service.yaml

microk8s kubectl get service
