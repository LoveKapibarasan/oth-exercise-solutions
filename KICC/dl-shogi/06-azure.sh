#!/bin/bash

ACR_NAME=shogiserver # no - in the name of ACR
RG_NAME=resource-group-1

az acr create --resource-group $RG_NAME --name $ACR_NAME --sku Basic --admin-enabled true

docker build -t ${ACR_NAME}.azurecr.io/shogiserver:v1.0.0 .
az acr login --name $ACR_NAME
docker push ${ACR_NAME}.azurecr.io/shogiserver:v1.0.0
ACR_PWD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)
az container create \
  --resource-group $RG_NAME \
  --name shogiserver-instance \
  --image $ACR_NAME.azurecr.io/shogiserver:v1.0.0 \
  --registry-login-server $ACR_NAME.azurecr.io \
  --registry-username $ACR_NAME \
  --registry-password $ACR_PWD \
  --dns-name-label shogi-app-$(date +%s) \
  --ports 4081 \
  --cpu 1 --memory 1.5 \
  --os-type Linux

az container show \
  --resource-group $RG_NAME \
  --name shogiserver-instance \
  --query "{FQDN:ipAddress.fqdn, IP:ipAddress.ip}" \
  --output table

# !! Even if you stop container you still have to pay for it
az container stop --resource-group $RG_NAME --name shogiserver-instance
# Delete every time
az container delete --resource-group $RG_NAME --name shogiserver-instance --yes

