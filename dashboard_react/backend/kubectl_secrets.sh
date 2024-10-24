#!/bin/bash
# Database credentials
pgsql_creds_path="/home/juaneshberger/Credentials/pgcreds.json"
# Django secret key
django_secret_key_path="/home/juaneshberger/Credentials/django_secret_key.txt"

# Create database secrets
creds=$(jq -r 'to_entries[] | "\(.key)=\(.value)"' $pgsql_creds_path)
for cred in $creds
do
  key=$(echo $cred | cut -f1 -d'=')
  value=$(echo $cred | cut -f2 -d'=' | tr -d '\r\n')
  
  secret_name="spx-django-$key"
  secret_key=$key
  
  microk8s kubectl delete secret $secret_name --ignore-not-found
  echo -n $value | microk8s kubectl create secret generic $secret_name --from-literal=$secret_key=$value
done

# Create Django-specific secrets
django_secret_key=$(cat $django_secret_key_path)
microk8s kubectl delete secret spx-django-secret-key --ignore-not-found
echo -n $django_secret_key | microk8s kubectl create secret generic spx-django-secret-key --from-literal=secret_key=$django_secret_key

# Create other Django settings secrets
microk8s kubectl delete secret spx-django-debug --ignore-not-found
echo -n "True" | microk8s kubectl create secret generic spx-django-debug --from-literal=debug=True

microk8s kubectl delete secret spx-django-allowed-hosts --ignore-not-found
echo -n "*" | microk8s kubectl create secret generic spx-django-allowed-hosts --from-literal=allowed_hosts="*"

sleep 3
microk8s kubectl get secrets
