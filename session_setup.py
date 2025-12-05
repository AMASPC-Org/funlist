import os
from datetime import timedelta

from config import settings


def configure_sessions(app, db, use_server_side: bool = True) -> None:
    """Apply session-related configuration."""
    secure_session_cookie = settings.get_bool("SESSION_COOKIE_SECURE", True)
    if os.environ.get("PROD"):
        secure_session_cookie = True

    app.config["SESSION_COOKIE_SECURE"] = secure_session_cookie
    app.config["SESSION_COOKIE_NAME"] = "__Host-funlist" if secure_session_cookie else "funlist_session"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if use_server_side:
        app.config["SESSION_TYPE"] = "sqlalchemy"
        app.config["SESSION_SQLALCHEMY"] = db
        app.config["SESSION_SQLALCHEMY_TABLE"] = "flask_sessions"
    else:
        app.config["SESSION_TYPE"] = "null"
