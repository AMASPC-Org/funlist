#!/usr/bin/env python3
"""Test script to verify OAuth configuration."""
import os

def test_oauth_config():
    """Check if OAuth environment variables are configured."""
    print("Testing OAuth Configuration...")
    print("=" * 50)
    
    # Check OAuth environment variables
    client_id = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
    session_secret = os.environ.get("SESSION_SECRET")
    
    results = {
        "GOOGLE_OAUTH_CLIENT_ID": "✅ Configured" if client_id else "❌ Missing",
        "GOOGLE_OAUTH_CLIENT_SECRET": "✅ Configured" if client_secret else "❌ Missing",
        "SESSION_SECRET": "✅ Configured" if session_secret else "❌ Missing"
    }
    
    for key, status in results.items():
        print(f"{key}: {status}")
    
    # Check redirect URL
    replit_domain = os.environ.get("REPLIT_DEV_DOMAIN", "localhost")
    redirect_url = f"https://{replit_domain}/google_login/callback"
    
    print(f"\nRedirect URL: {redirect_url}")
    print("Make sure this URL is added to your Google OAuth configuration.")
    
    # Overall status
    all_configured = all("✅" in status for status in results.values())
    if all_configured:
        print("\n✅ OAuth is properly configured!")
        print("The OAuth should work once the server is running properly.")
        return True
    else:
        print("\n❌ OAuth is missing some configuration.")
        print("Please check the missing environment variables.")
        return False

if __name__ == "__main__":
    test_oauth_config()