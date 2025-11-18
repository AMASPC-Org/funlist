
from flask import Blueprint, jsonify, url_for
import os

debug = Blueprint("debug", __name__)

@debug.route("/_health/oauth")
def oauth_health():
    """Health check endpoint to verify OAuth configuration"""
    required_vars = ["GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "FLASK_SECRET_KEY"]
    ok = all(os.getenv(k) for k in required_vars)
    
    app_url = os.getenv('APP_URL', '')
    
    return jsonify({
        "env_ok": ok,
        "missing_vars": [k for k in required_vars if not os.getenv(k)],
        "login_route_exists": True,
        "callback_hint": f"{app_url}/google_login/callback"
    }), (200 if ok else 500)
