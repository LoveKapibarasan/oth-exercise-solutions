#!/bin/bash

# Search images
# https://learn.microsoft.com/en-us/cli/azure/vm/image?view=azure-cli-latest#az-vm-image-list-offers
az vm image list-offers --location japaneast --publisher Canonical --output table

# Check SSH key
az sshkey list --output table

# generete SSH key
ssh-keygen -t ed25519 -f ~/.ssh/azure_ed # backup this via google drive

# https://learn.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-cli
export RG_NAME="resource-group-1"
export VM_NAME="vm-1"
export VNET_NAME="vnet-1"
export SUBNET_NAME="PublicSubnet"
# URN(uniform Resource Name): https://az-vm-image.info/
export VM_IMAGE="Canonical:ubuntu-24_04-lts:server:latest"

az vm create \
    --resource-group $RG_NAME \
    --name $VM_NAME \
    --image $VM_IMAGE \
    --size Standard_D2s_v3 \
    --vnet-name $VNET_NAME \
    --subnet $SUBNET_NAME \
    --admin-username azureuser \
    --ssh-key-values @~/.ssh/azure_ed.pub 
  # --generate-ssh-keys
  # --ssh-key-values MyAzureSSHKeyName
  # --size Standard_B1s, B2s \ : unavailable
az vm list-sizes --location japaneast --output table
# SKU: Stock keeping unit  

# Check
az vm list --resource-group $RG_NAME --output table

#  === Delete ===
# 1. Deallocate (Storage, IP fee are charged)
az vm deallocate --resource-group $RG_NAME --name $VM_NAME
az vm get-instance-view --resource-group $RG_NAME --name $VM_NAME --query "instanceView.statuses[1].displayStatus" -o tsv

# 2. Delete
az group delete --name $RG_NAME

# === Restart ===
az vm start --resource-group $RG_NAME --name $VM_NAME
# Check new ip address
az vm list-ip-addresses --resource-group $RG_NAME --name $VM_NAME --output table