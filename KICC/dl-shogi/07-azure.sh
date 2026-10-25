# 1. Install Azure App Service on VSCode
# 2. Sign In

az webapp list-runtimes --os Linux | grep -i node

# 22 or 24
export APP_NAME="shogihome"
export RG_NAME="resource-group-1"

az webapp up --runtime "NODE:22-lts" --name $APP_NAME --location "japaneast"
# Access via https://shogihome.azurewebsites.net

# Setting. -> Configuration -> Stack Setting
az webapp config set --resource-group $RG_NAME --name $APP_NAME --startup-file "/home/site/wwwroot/entrypoint.sh"


# Increase WEBSITES_CONTAINER_START_TIME_LIMIT