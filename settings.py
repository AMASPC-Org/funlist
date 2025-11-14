from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Set

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DB_PATH = PROJECT_ROOT / "instance" / "funlist.db"
DEFAULT_GOOGLE_MAPS_API_KEY = "AIzaSyDRkUhORhaKILaPN0-qi9YndDShVov0DVE"
ENV_FILE = Path(os.environ.get("FUNLIST_ENV_FILE", PROJECT_ROOT / ".env"))


def _load_env_file() -> Dict[str, str]:
    """Load key/value pairs from .env into os.environ without clobbering real env vars."""
    if not ENV_FILE.exists():
        return {}

    loaded: Dict[str, str] = {}
    for raw_line in ENV_FILE.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if not key:
            continue

        # Do not override actual environment variables that were set outside the file.
        loaded_value = os.environ.setdefault(key, value)
        loaded[key] = loaded_value

    return loaded


_load_env_file()


def _default_database_url() -> str:
    sqlite_path = DEFAULT_DB_PATH
    return os.environ.get("DATABASE_URL", f"sqlite:///{sqlite_path}")


def _default_google_maps_key() -> str:
    return os.environ.get("GOOGLE_MAPS_API_KEY", DEFAULT_GOOGLE_MAPS_API_KEY)


def _default_admin_emails() -> Set[str]:
    raw = os.environ.get("FIREBASE_ADMIN_EMAILS", "ryan@funlist.ai")
    return {email.strip().lower() for email in raw.split(",") if email.strip()}


@dataclass
class Settings:
    flask_app: str = field(default_factory=lambda: os.environ.get("FLASK_APP", "main.py"))
    flask_env: str = field(default_factory=lambda: os.environ.get("FLASK_ENV", "development"))
    flask_secret_key: str = field(default_factory=lambda: os.environ.get("FLASK_SECRET_KEY", "change-me"))
    database_url: str = field(default_factory=_default_database_url)
    admin_emails: Set[str] = field(default_factory=_default_admin_emails)
    google_maps_api_key: str = field(default_factory=_default_google_maps_key)
    firebase_credentials_path: str = field(default_factory=lambda: os.environ.get("FIREBASE_CREDENTIALS_PATH", ""))
    firebase_credentials_json: str = field(default_factory=lambda: os.environ.get("FIREBASE_CREDENTIALS_JSON", ""))
    firebase_api_key: str = field(default_factory=lambda: os.environ.get("FIREBASE_API_KEY", ""))
    firebase_auth_domain: str = field(default_factory=lambda: os.environ.get("FIREBASE_AUTH_DOMAIN", ""))
    firebase_project_id: str = field(default_factory=lambda: os.environ.get("FIREBASE_PROJECT_ID", ""))
    firebase_app_id: str = field(default_factory=lambda: os.environ.get("FIREBASE_APP_ID", ""))
    firebase_messaging_sender_id: str = field(default_factory=lambda: os.environ.get("FIREBASE_MESSAGING_SENDER_ID", ""))
    firebase_storage_bucket: str = field(default_factory=lambda: os.environ.get("FIREBASE_STORAGE_BUCKET", ""))
    firebase_measurement_id: str = field(default_factory=lambda: os.environ.get("FIREBASE_MEASUREMENT_ID", ""))


settings = Settings()


def reload_settings() -> Settings:
    """Reload .env values and return a fresh Settings instance."""
    _load_env_file()
    global settings
    settings = Settings()
    return settings


__all__ = ["settings", "reload_settings", "Settings", "ENV_FILE", "PROJECT_ROOT"]
