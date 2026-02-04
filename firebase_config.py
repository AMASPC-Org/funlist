import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from config import settings

_db = None

def init_firebase():
    """Initialize Firebase Admin SDK and return firestore client."""
    global _db
    if _db is not None:
        return _db

    # Check for credentials in settings (from .env)
    cred_json = settings.get("FIREBASE_CREDENTIALS_JSON")
    project_id = settings.get("FIREBASE_PROJECT_ID", "ama-ecosystem-prod")

    if cred_json:
        try:
            cred_dict = json.loads(cred_json)
            cred = credentials.Certificate(cred_dict)
        except Exception as e:
            print(f"Error parsing FIREBASE_CREDENTIALS_JSON: {e}")
            cred = credentials.ApplicationDefault()
    else:
        # Fallback to Application Default Credentials
        cred = credentials.ApplicationDefault()

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            'projectId': project_id,
        })
    
    _db = firestore.client()
    return _db

def get_db():
    if _db is None:
        return init_firebase()
    return _db
