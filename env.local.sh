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
export FIREBASE_CREDENTIALS_PATH="${FIREBASE_CREDENTIALS_PATH:-}"
export FIREBASE_CREDENTIALS_JSON="${FIREBASE_CREDENTIALS_JSON:-}"
export FIREBASE_API_KEY="${FIREBASE_API_KEY:-}"
export FIREBASE_AUTH_DOMAIN="${FIREBASE_AUTH_DOMAIN:-}"
export FIREBASE_PROJECT_ID="${FIREBASE_PROJECT_ID:-}"
export FIREBASE_APP_ID="${FIREBASE_APP_ID:-}"
export FIREBASE_MESSAGING_SENDER_ID="${FIREBASE_MESSAGING_SENDER_ID:-}"
export FIREBASE_STORAGE_BUCKET="${FIREBASE_STORAGE_BUCKET:-}"
export FIREBASE_MEASUREMENT_ID="${FIREBASE_MEASUREMENT_ID:-}"
export FIREBASE_ADMIN_EMAILS="${FIREBASE_ADMIN_EMAILS:-ryan@funlist.ai}"

cat <<EOF
Environment configured:
  FLASK_APP=$FLASK_APP
  FLASK_ENV=$FLASK_ENV
  FLASK_SECRET_KEY=$FLASK_SECRET_KEY
  DATABASE_URL=$DATABASE_URL
  GOOGLE_MAPS_API_KEY=$GOOGLE_MAPS_API_KEY
  FIREBASE_PROJECT_ID=$FIREBASE_PROJECT_ID
  FIREBASE_AUTH_DOMAIN=$FIREBASE_AUTH_DOMAIN
  FIREBASE_API_KEY=$FIREBASE_API_KEY

Firebase Authentication powers login/signup. Make sure the Firebase variables above (plus either FIREBASE_CREDENTIALS_PATH or FIREBASE_CREDENTIALS_JSON) are set before running the app.
EOF
