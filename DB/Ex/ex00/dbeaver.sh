#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/../../../util.sh"
HOME=$(get_user_home)
# https://github.com/dbeaver/dbeaver/wiki/Build-from-sources
root_check

if is_command pacman; then
        sudo pacman -S --needed --noconfirm git jdk-openjdk maven
elif is_command apt; then
        sudo apt update
        sudo apt install -y git openjdk-21-jdk maven
else
	exit 1
fi

cd
# mirror
git clone -o upstream https://github.com/dbeaver/dbeaver.git dbeaver
cd dbeaver

# build
cd tools
./build.sh

ls -la product/community/target/products/
cd ..

DBEAVER_PATH=$(pwd)/product/community/target/products/org.jkiss.dbeaver.core.product/linux/gtk/x86_64/dbeaver/dbeaver

chmod +x "$DBEAVER_PATH"
sudo rm -f /usr/local/bin/dbeaver
sudo ln -s "$DBEAVER_PATH" /usr/local/bin/dbeaver


read -p "Enter your username: " USER
sudo chown -R $USER:$USER /usr/local/bin/dbeaver
sudo chown -R $USER:$USER "${HOME}/dbeaver"
cd $SCRIPT_DIR
