#!/bin/bash

# Display the current list of storage accounts
az storage account list --output table

# Variable definitions
RG_NAME="resource-group-1" 
LOC="japaneast"
# Generate a unique name using the current date
ST_NAME="storage$(date +%Y%m%d)unique"
CONTAINER_NAME="data"

export ST_NAME=$(az storage account list --query "[0].name" --output tsv)

# Create a new storage account
az storage account create \
  --name "$ST_NAME" \
  --resource-group "$RG_NAME" \
  --location "$LOC" \
  --sku Standard_LRS

# Create a blob container
az storage container create \
  --name "$CONTAINER_NAME" \
  --account-name "$ST_NAME"

# Upload test: Create a dummy file and upload it
echo "hello azure storage!" > test.txt

az storage blob upload \
  --account-name "$ST_NAME" \
  --container-name "$CONTAINER_NAME" \
  --name "uploaded-test.txt" \
  --file "test.txt" \
  --auth-mode key

az storage blob upload-batch \
  --account-name "$ST_NAME" \
  --destination "$CONTAINER_NAME" \
  --source "." \
  --pattern "*.txt" \
  --auth-mode key

# Cleanup local file and list blobs in the container
rm test.txt
az storage blob list \
  --account-name "$ST_NAME" \
  --container-name "$CONTAINER_NAME" \
  --output table



az storage blob upload-batch \
  --account-name "$ST_NAME" \
  --destination "$CONTAINER_NAME" \
  --source "." \
  --pattern "*.hcpe" \
  --auth-mode key

# delete files
az storage blob delete-batch \
  --account-name "$ST_NAME" \
  --source "$CONTAINER_NAME" \
  --auth-mode key

# delete container
az storage container delete \
  --account-name "$ST_NAME" \
  --name "$CONTAINER_NAME" \
  --auth-mode key