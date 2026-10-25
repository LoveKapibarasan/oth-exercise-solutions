query_hasura() {
  local query="$1"
  local url="${2:-"${HASURA_URL}"}"
  local secret="${3:-"${HASURA_SECRET}"}"
  
  curl -s -X POST "$url" \
    -H "Content-Type: application/json" \
    -H "x-hasura-admin-secret: $secret" \
    -d "{\"query\": \"$query\"}" | jq .
}
