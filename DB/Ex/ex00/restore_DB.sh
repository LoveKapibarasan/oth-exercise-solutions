#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/../../../util.sh"
source "${SCRIPT_DIR}/../data/.env.local"

PSQL_R="sudo -u postgres psql -h localhost -p $PGPORT"

$PSQL_R -c "DROP DATABASE IF EXISTS $PGDATABASE;"
$PSQL_R -c "CREATE DATABASE $PGDATABASE OWNER $PGUSER;"

DATA_PATH="${SCRIPT_DIR}/../data" 
psql -q -h localhost -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "${DATA_PATH}/drop.sql"
psql -q -h localhost -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "${DATA_PATH}/largeRelations.sql"

echo "Database recreated successfully!"
