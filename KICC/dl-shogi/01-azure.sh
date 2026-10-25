#!/bin/bash

# https://learn.microsoft.com/en-us/cli/azure/?view=azure-cli-latest
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
# winget install --exact --id Microsoft.AzureCLI: for windows
az upgrade
az login --use-device-code #  --tenant <tenant-id>

# Check my tenant
az account tenant list --output table
# Check the resource list
az resource list --resource-group resource-group-1 --output table

# Check locations
az account list-locations
az account list-locations \
  --query "[?contains(displayName, 'Japan')].{Name:name, az account tenant list --output tableDisplayName:displayName}" \
  --output table

# Create resource group in JapanEast
az group create --name resource-group-1 --location japaneast
az group list --output table

# Initialize VNet
az network vnet create \
  --resource-group resource-group-1 \
  --name vnet-1 \
  --address-prefix 10.0.0.0/16 \
  --subnet-name PublicSubnet \
  --subnet-prefix 10.0.1.0/24
az network vnet list --resource-group resource-group-1 --output table