import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

# Load .env automatically so modules can rely on os.environ
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)


class Settings:
    """Helper for accessing environment variables with optional validation."""

    def __init__(self) -> None:
        self.base_dir = BASE_DIR

    def get(self, key: str, default: Optional[str] = None, *, required: bool = False) -> Optional[str]:
        value = os.environ.get(key, default)
        if required and not value:
            raise RuntimeError(f"{key} environment variable must be set")
        return value

    def get_bool(self, key: str, default: bool = False) -> bool:
        value = os.environ.get(key)
        if value is None:
            return default
        return str(value).lower() in {"1", "true", "yes", "on"}


settings = Settings()
