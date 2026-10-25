#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/../../../util.sh"
HOME=$(get_user_home)

# https://fbim.oth-regensburg.de/wiki/doku.php?id=public:postgres
SERVER=zeus.hs-regensburg.de # or hera.hs-regensburg.de 
root_check

if is_command nordvpn;then
	sudo nordvpn disconnect
fi

if is_command openfortivpn;then
	sudo openfortivpn -c /etc/openfortivpn/config &
	VPN_PID=$!
	sleep 8
fi

read -p "Enter your OTH username: " OTH_USERNAME
read -p "Enter database name (default: $OTH_USERNAME): " DBNAME
read -ps "Enter your new OTH DB password: " OTH_PASSWORD

export PGPASSWORD="$OTH_USERNAME" 
# Large Data Version
URL1=https://db-book.com/university-lab-dir/sample_tables-dir/DDL+drop.sql
URL2=https://db-book.com/university-lab-dir/sample_tables-dir/largeRelations/largeRelationsInsertFile.sql

# default
DATA_PATH="${SCRIPT_DIR}/../data" 
wget "$URL1" -O "${DATA_PATH}/drop.sql"
wget "$URL2" -O "${DATA_PATH}/largeRelations.sql"

psql -q -h "$SERVER" -p 5432 -U "$OTH_USERNAME" -d "$DBNAME" -f "${DATA_PATH}/drop.sql"
psql -q -h "$SERVER" -p 5432 -U "$OTH_USERNAME" -d "$DBNAME" -f "${DATA_PATH}/largeRelations.sql"

# Change initial password 
psql -h hera.hs-regensburg.de -p 5432 -U "$OTH_USERNAME" -d "$DBNAME" \
        -c "ALTER ROLE $OTH_USERNAME PASSWORD '$OTH_PASSWORD';"

#=====
read -p "Enter username: " L_USERNAME
echo
read -sp "Enter password: " L_PASSWORD
echo
read -sp "Enter DBNAME: " DBNAME
echo
read -p "Enter local postgre port: " P_PORT

export PGPASSWORD="$L_PASSWORD" 

sudo sed -i "s/^#*port = .*/port = $P_PORT/" /var/lib/postgres/data/postgresql.conf
sudo systemctl restart postgresql
sudo -u postgres psql -h localhost -p "$P_PORT" -c "CREATE USER $L_USERNAME WITH PASSWORD '$L_PASSWORD';"
sudo -u postgres psql -h localhost -p "$P_PORT" -c "CREATE DATABASE $DBNAME OWNER $L_USERNAME;"
## Check
psql -h localhost -p "$P_PORT" -U postgres -c "\l"
psql -h localhost -p "$P_PORT" -U postgres -c "\du"

echo "Granting privileges..."
sudo -u postgres psql -h localhost -p "$P_PORT" -c "GRANT ALL PRIVILEGES ON DATABASE $DBNAME TO $L_USERNAME;"

PGPASSWORD="$L_PASSWORD" psql -q -h localhost -p "$P_PORT" -U "$L_USERNAME" -d "$DBNAME" -f "${DATA_PATH}/drop.sql"
PGPASSWORD="$L_PASSWORD" psql -q -h localhost -p "$P_PORT" -U "$L_USERNAME" -d "$DBNAME" -f "${DATA_PATH}/largeRelations.sql"


# save 1
REAL_USER=${SUDO_USER:-$USER}

echo "localhost:$P_PORT:${DBNAME}:${L_USERNAME}:${L_PASSWORD}" > "${HOME}/.pgpass"
chown $REAL_USER:$REAL_USER "${HOME}/.pgpass"
chmod 600 "${REAL_HOME}/.pgpass"
cat "${HOME}/.pgpass"

# save 2
ENV_FILE="${DATA_PATH}/.env.local"
cat > "$ENV_FILE" << EOF
# PostgreSQL Local Configuration
# Generated on $(date)

#=== Local Database ===
PGHOST=localhost
PGPORT=$P_PORT
PGDATABASE=$DBNAME
PGUSER=$L_USERNAME
PGPASSWORD=$L_PASSWORD

#=== Remote Database ===
REMOTE_HOST=hera.hs-regensburg.de
REMOTE_USER=$OTH_USERNAME
REMOTE_DATABASE=$DBNAME
OTH_PGPASSWORD=$OTH_PASSWORD
EOF

chown $REAL_USER:$REAL_USER "$ENV_FILE"
chmod 600 "$ENV_FILE"
# Clean Up
sudo kill $VPN_PID
cd $SCRIPT_DIR

