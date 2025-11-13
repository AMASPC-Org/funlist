#!/usr/bin/env bash
# Usage: source env.local.sh
# Sets the minimum environment needed to boot the Funlist Flask app.

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    echo "Please source this script so the exports stay in your current shell:"
    echo "  source env.local.sh"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}"
DB_PATH="${PROJECT_ROOT}/instance/funlist.db"

export FLASK_APP="main.py"
export FLASK_ENV="${FLASK_ENV:-development}"
export FLASK_SECRET_KEY="${FLASK_SECRET_KEY:-change-me}"
export DATABASE_URL="${DATABASE_URL:-sqlite:///${DB_PATH}}"
export GOOGLE_MAPS_API_KEY="${GOOGLE_MAPS_API_KEY:-AIzaSyCMEtAgms0HALTBraFW9uM7Yuj6raNfnDs}"

cat <<EOF
Environment configured:
  FLASK_APP=$FLASK_APP
  FLASK_ENV=$FLASK_ENV
  FLASK_SECRET_KEY=$FLASK_SECRET_KEY
  DATABASE_URL=$DATABASE_URL
  GOOGLE_MAPS_API_KEY=$GOOGLE_MAPS_API_KEY

Remember to replace REPLACE_WITH_REAL_KEY in env.local.sh with your Google Maps key.
EOF
