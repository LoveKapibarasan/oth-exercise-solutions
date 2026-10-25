#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/../../../util.sh"
HOME=$(get_user_home)

root_check

if is_command pacman; then
sudo pacman -S --needed --noconfirm base-devel readline zlib \
        flex bison libxml2 libxslt openssl \
        autoconf automake libtool pkgconf
elif is_command apt; then
# Debian/Ubuntu
sudo apt install build-essential libreadline-dev zlib1g-dev \
  flex bison libxml2-dev libxslt-dev libssl-dev \
  autoconf automake libtool pkg-config
else
	exit 1
fi

# GitHub mirror
cd 
git clone -o upstream https://github.com/postgres/postgres.git
cd postgres
git checkout master

# Configure
./configure --help
./configure --prefix=/usr/local/pgsql   --with-python --with-openssl 
# --prefix=/usr/local/pgsql =  install Postgre at  

# Build 
make -j$(nproc)

# Test
make check

# Install
sudo make install

sudo docker ps | grep postgres | awk '{print $1}' | xargs -r sudo docker stop
sudo systemctl start postgresql
sudo systemctl enable postgresql

cd $SCRIPT_DIR
