import json
import logging
import os
from typing import Any, Dict, Optional

import firebase_admin
from firebase_admin import auth, credentials

logger = logging.getLogger(__name__)


class FirebaseAuthError(Exception):
    """Raised when Firebase authentication fails."""


_firebase_app: Optional[firebase_admin.App] = None


def _load_credentials() -> credentials.Certificate:
    """Load Firebase credentials from either a file path or raw JSON."""
    cred_path = os.environ.get("FIREBASE_CREDENTIALS_PATH")
    raw_json = os.environ.get("FIREBASE_CREDENTIALS_JSON")

    if cred_path:
        if not os.path.exists(cred_path):
            raise FirebaseAuthError(
                f"Firebase credentials file not found at {cred_path}"
            )
        return credentials.Certificate(cred_path)

    if raw_json:
        try:
            cred_dict = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            raise FirebaseAuthError("Invalid FIREBASE_CREDENTIALS_JSON payload.") from exc

        # Ensure multi-line private keys are formatted correctly
        if "private_key" in cred_dict:
            cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n")
        return credentials.Certificate(cred_dict)

    # Fall back to application default credentials if available
    try:
        return credentials.ApplicationDefault()
    except Exception as exc:  # pragma: no cover - bubbled to caller
        raise FirebaseAuthError(
            "Firebase credentials are not configured. "
            "Set FIREBASE_CREDENTIALS_PATH or FIREBASE_CREDENTIALS_JSON."
        ) from exc


def initialize_firebase() -> Optional[firebase_admin.App]:
    """Initialize the Firebase Admin SDK once and reuse the app."""
    global _firebase_app
    if _firebase_app:
        return _firebase_app

    try:
        credential = _load_credentials()
    except FirebaseAuthError as exc:
        logger.error("Failed to load Firebase credentials: %s", exc)
        raise

    if firebase_admin._apps:
        _firebase_app = firebase_admin.get_app()
    else:
        _firebase_app = firebase_admin.initialize_app(credential)

    logger.info("Firebase Admin SDK initialized.")
    return _firebase_app


def verify_firebase_token(id_token: str) -> Dict[str, Any]:
    """Verify the provided Firebase ID token and return its decoded payload."""
    if not id_token:
        raise FirebaseAuthError("Missing Firebase ID token.")

    app = initialize_firebase()
    try:
        return auth.verify_id_token(id_token, app=app)
    except auth.ExpiredIdTokenError as exc:
        raise FirebaseAuthError("Your session has expired. Please sign in again.") from exc
    except auth.InvalidIdTokenError as exc:
        raise FirebaseAuthError("Invalid Firebase ID token.") from exc
    except auth.RevokedIdTokenError as exc:
        raise FirebaseAuthError("This Firebase ID token has been revoked.") from exc
    except ValueError as exc:
        raise FirebaseAuthError("Unable to parse Firebase ID token.") from exc
    except Exception as exc:  # pragma: no cover - logged for observability
        logger.exception("Unexpected Firebase verification error.")
        raise FirebaseAuthError("Unable to verify Firebase ID token.") from exc


def get_firebase_client_config() -> Dict[str, str]:
    """Expose the Firebase client configuration for the front-end."""
    keys = {
        "apiKey": os.environ.get("FIREBASE_API_KEY"),
        "authDomain": os.environ.get("FIREBASE_AUTH_DOMAIN"),
        "projectId": os.environ.get("FIREBASE_PROJECT_ID"),
        "storageBucket": os.environ.get("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": os.environ.get("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": os.environ.get("FIREBASE_APP_ID"),
        "measurementId": os.environ.get("FIREBASE_MEASUREMENT_ID"),
    }
    # Remove empty values so the client receives a clean payload
    return {k: v for k, v in keys.items() if v}

