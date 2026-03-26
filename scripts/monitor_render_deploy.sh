#!/usr/bin/env bash
set -euo pipefail

RENDER_API_KEY=${RENDER_API_KEY:-}
SERVICE_ID=${SERVICE_ID:-}

if [ -z "$RENDER_API_KEY" ] || [ -z "$SERVICE_ID" ]; then
  echo "Usage: export RENDER_API_KEY=...; export SERVICE_ID=...; bash scripts/monitor_render_deploy.sh"
  exit 1
fi

prev_status=""
echo "Starting Render deploy monitor for service $SERVICE_ID"
while true; do
  now=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  resp=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" "https://api.render.com/v1/services/$SERVICE_ID/deploys") || { echo "$now - error listing deploys"; sleep 30; continue; }
  latest=$(python3 - <<PY
import sys,json
try:
    arr=json.load(sys.stdin)
    if not arr:
        print("")
    else:
        print(arr[0]['deploy']['id'])
except Exception:
    print("")
PY
<<<"$resp")

  if [ -z "$latest" ]; then
    echo "$now - no deploys found"
    sleep 30
    continue
  fi

  deploy_json=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" "https://api.render.com/v1/deploys/$latest") || { echo "$now - error fetching deploy $latest"; sleep 30; continue; }
  status=$(python3 - <<PY
import sys,json
try:
    j=json.load(sys.stdin)
    print(j.get('status',''))
except Exception:
    print('')
PY
<<<"$deploy_json")

  if [ "$status" != "$prev_status" ]; then
    echo "$now - deploy $latest status changed: $status"
    prev_status=$status
    mkdir -p deploy-logs
    echo "$deploy_json" > deploy-logs/$latest.json || true
    echo "$now - saved deploy JSON to deploy-logs/$latest.json"
    # try to fetch raw output if available
    raw=$(curl -s -H "Authorization: Bearer $RENDER_API_KEY" "https://api.render.com/v1/deploys/$latest/raw-output" || true)
    if [ -n "$raw" ]; then
      echo "$raw" > deploy-logs/$latest-raw.txt || true
      echo "$now - saved raw output to deploy-logs/$latest-raw.txt"
    fi

    if [ "$status" = "build_failed" ]; then
      echo "$now - Build failed for deploy $latest. Saved logs under deploy-logs/; please inspect."
    elif [ "$status" = "deployed" ] || [ "$status" = "succeeded" ]; then
      echo "$now - Deploy $latest succeeded"
    fi
  fi

  sleep 30
done
