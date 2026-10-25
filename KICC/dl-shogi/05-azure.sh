#!/bin/bash


az extension add -n ml
az extension update --name ml

export WORKSPACE_NAME=dl-shogi
export RESOURCE_GROUP=resource-group-1
export LOCATION=japaneast

az ml workspace create --name "$WORKSPACE_NAME" --resource-group "$RESOURCE_GROUP" --location "$LOCATION"
# https://learn.microsoft.com/en-us/cli/azure/ml/compute?view=azure-cli-latest#az-ml-compute-create
az ml compute create --name gpu-instance \
    --resource-group "$RESOURCE_GROUP" \
    --workspace-name "$WORKSPACE_NAME" \
    --type ComputeInstance \
    --size Standard_NC6s_v3 \
    --location "$LOCATION"

# https://ml.azure.com/quota/
# increase quota: Standard NCv3 Family Cluster Dedicated vCPUs
az ml compute create --name cpu-test-instance \
    --resource-group "$RESOURCE_GROUP" \
    --workspace-name "$WORKSPACE_NAME" \
    --type ComputeInstance \
    --size Standard_DS3_v2 \
    --location "$LOCATION"

# ssh
# https://learn.microsoft.com/en-us/azure/machine-learning/how-to-access-terminal?view=azureml-api-2
ssh-keygen -t ed25519 -f ./ml_key -N ""
az ml compute update --name cpu-test-instance \
    -g resource-group-1 -w dl-shogi \
    --set ssh_settings.ssh_key_value="$(cat ./ml_key.pub)"


lscpu && free -h

az ml compute show --name gpu-instance --resource-group "$RESOURCE_GROUP" --workspace-name "$WORKSPACE_NAME"

# Stop compute instance
az ml compute stop --name gpu-instance --resource-group "$RESOURCE_GROUP" --workspace-name "$WORKSPACE_NAME"
# Delete compute instance
az ml compute delete --name gpu-instance --resource-group "$RESOURCE_GROUP" --workspace-name "$WORKSPACE_NAME"