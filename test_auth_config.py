#!/usr/bin/env python3
"""Smoke test for Firebase Auth configuration."""

import os
import requests


def check_env():
    print("Firebase Auth Configuration")
    print("=" * 50)
    required = [
        "FIREBASE_ENABLED",
        "FIREBASE_PROJECT_ID",
        "FIREBASE_API_KEY",
        "FIREBASE_AUTH_DOMAIN",
        "FIREBASE_APP_ID",
    ]
    for key in required:
        value = os.environ.get(key)
        status = "✅" if value else "❌"
        print(f"{key}: {status}")
    print()


def check_health():
    base_url = os.environ.get("APP_URL") or "http://localhost:5000"
    url = f"{base_url.rstrip('/')}/_health/oauth"
    try:
        resp = requests.get(url, timeout=5)
        if resp.ok:
            print(f"Health endpoint OK ({resp.status_code})")
            print(resp.json())
        else:
            print(f"Health endpoint returned {resp.status_code}")
            print(resp.text)
    except Exception as exc:  # noqa: BLE001
        print(f"Health check failed: {exc}")


if __name__ == "__main__":
    check_env()
    check_health()
