
from flask import Blueprint, jsonify, url_for
import os

debug = Blueprint("debug", __name__)

@debug.route("/_health/oauth")
def oauth_health():
    """Health check endpoint to verify Firebase auth configuration"""
    required_vars = ["FIREBASE_ENABLED", "FIREBASE_PROJECT_ID", "FIREBASE_API_KEY"]
    ok = all(os.getenv(k) for k in required_vars) and os.getenv("FIREBASE_ENABLED", "").lower() in {"1", "true", "yes", "on"}
    
    return jsonify({
        "env_ok": ok,
        "missing_vars": [k for k in required_vars if not os.getenv(k)],
        "login_route_exists": True,
        "firebase_enabled": os.getenv("FIREBASE_ENABLED"),
        "token_endpoint": url_for('firebase_auth.firebase_login', _external=True)
    }), (200 if ok else 500)
