docker build -t juanestebanberger/spx-tableau:latest .

docker push juanestebanberger/spx-tableau:latest

kubectl delete deployment spx-tableau-deployment --ignore-not-found=true
kubectl apply -f deployment.yaml
kubectl delete service spx-tableau-service --ignore-not-found=true
kubectl apply -f service.yaml

kubectl get service
