# Firebase-based authentication for Google sign-in using Firebase Auth ID tokens.
# The frontend obtains an ID token from Firebase (Google provider) and posts it
# to these endpoints; the backend verifies the token and signs the user in.

import json
import secrets
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials
from flask import Blueprint, current_app, jsonify, request, session, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import or_
from werkzeug.security import generate_password_hash

from config import settings
from db_init import db
from models import User

firebase_app = None


def firebase_enabled() -> bool:
    return settings.get_bool("FIREBASE_ENABLED", False)


def _load_credentials() -> Optional[credentials.Certificate]:
    """Load Firebase credentials from JSON string or file path."""
    credential_json = settings.get("FIREBASE_CREDENTIALS_JSON")
    if credential_json:
        try:
            return credentials.Certificate(json.loads(credential_json))
        except json.JSONDecodeError:
            pass

    credential_path = settings.get("FIREBASE_CREDENTIALS_PATH") or "firebase-service-account.json"
    path_obj = Path(credential_path)
    if path_obj.exists():
        return credentials.Certificate(path_obj)
    return None


def init_firebase_app(logger=None):
    """Initialize Firebase Admin SDK for verifying ID tokens."""
    global firebase_app
    if firebase_app:
        return firebase_app

    if not firebase_enabled():
        raise RuntimeError("Firebase auth is not enabled. Set FIREBASE_ENABLED=true to enable.")

    if firebase_admin._apps:
        firebase_app = firebase_admin.get_app()
        return firebase_app

    cred = _load_credentials()
    if not cred:
        raise RuntimeError("Firebase credentials not provided. Set FIREBASE_CREDENTIALS_JSON or FIREBASE_CREDENTIALS_PATH.")

    firebase_app = firebase_admin.initialize_app(
        cred,
        {"projectId": settings.get("FIREBASE_PROJECT_ID")}
    )
    if logger:
        logger.info("Firebase Admin initialized for project %s", settings.get("FIREBASE_PROJECT_ID"))
    return firebase_app


firebase_auth_bp = Blueprint("firebase_auth", __name__, url_prefix="/auth/firebase")


def _split_name(full_name: str) -> Tuple[str, str]:
    if not full_name:
        return "", ""
    parts = full_name.split(" ", 1)
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[1]


@firebase_auth_bp.route("/login", methods=["POST"])
def firebase_login():
    if not firebase_enabled():
        return jsonify({"success": False, "message": "Firebase auth is not enabled."}), 503

    data = request.get_json() or {}
    id_token = data.get("idToken")
    next_url = data.get("next") or url_for("index")

    if not id_token:
        return jsonify({"success": False, "message": "Missing Firebase ID token."}), 400

    try:
        app = init_firebase_app(current_app.logger if current_app else None)
        decoded_token = firebase_auth.verify_id_token(id_token, app=app, check_revoked=True)
        uid = decoded_token.get("uid")
        email = decoded_token.get("email")

        if not uid or not email:
            return jsonify({"success": False, "message": "Invalid Firebase token payload."}), 400

        first_name, last_name = _split_name(decoded_token.get("name", ""))
        email_verified = bool(decoded_token.get("email_verified"))

        user = User.query.filter(
            or_(User.oauth_provider_id == uid, User.email == email)
        ).first()

        if not user:
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password_hash=generate_password_hash(secrets.token_hex(16)),
                oauth_provider="google",
                oauth_provider_id=uid,
                email_verified=email_verified,
            )
            db.session.add(user)
        else:
            if not user.oauth_provider_id:
                user.oauth_provider_id = uid
            if not user.oauth_provider:
                user.oauth_provider = "google"
            if email_verified:
                user.email_verified = True
            if first_name and not user.first_name:
                user.first_name = first_name
            if last_name and not user.last_name:
                user.last_name = last_name

        user.last_login = datetime.utcnow()
        db.session.commit()

        login_user(user, remember=True)
        return jsonify({"success": True, "redirect": next_url})
    except Exception as exc:
        if current_app:
            current_app.logger.exception("Firebase sign-in failed: %s", exc)
        return jsonify({"success": False, "message": "Google sign-in failed. Please try again."}), 401


@firebase_auth_bp.route("/logout", methods=["POST"])
@login_required
def firebase_logout():
    logout_user()
    session.clear()
    return jsonify({"success": True, "redirect": url_for("index")})
