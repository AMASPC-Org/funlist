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
#!/usr/bin/env python3
"""
OAuth Integration Test Suite
Tests OAuth login flows, session handling, and protected routes
"""
import os
import sys
import requests
from urllib.parse import urlparse, parse_qs

def test_oauth_endpoints():
    """Test OAuth endpoints and configuration"""
    base_url = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')
    protocol = 'https' if 'replit.dev' in base_url else 'http'
    app_url = f"{protocol}://{base_url}"
    
    print("\n" + "="*60)
    print("OAuth Integration Test Suite")
    print("="*60)
    
    # Test 1: Check OAuth login redirects
    print("\n📋 Test 1: OAuth Login Redirects")
    print("-" * 60)
    
    for provider in ['google', 'github']:
        try:
            url = f"{app_url}/auth/{provider}/login"
            response = requests.get(url, allow_redirects=False, timeout=5)
            
            if response.status_code in [302, 303, 307]:
                location = response.headers.get('Location', '')
                if provider in location.lower() or 'oauth' in location.lower():
                    print(f"✅ {provider.title()}: Redirect working (→ {location[:50]}...)")
                else:
                    print(f"⚠️  {provider.title()}: Unexpected redirect ({location[:50]}...)")
            else:
                print(f"❌ {provider.title()}: Expected redirect, got {response.status_code}")
                
        except Exception as e:
            print(f"❌ {provider.title()}: {str(e)}")
    
    # Test 2: Protected route (should require auth)
    print("\n📋 Test 2: Protected Route Access")
    print("-" * 60)
    
    try:
        # Test without authentication
        response = requests.get(f"{app_url}/profile", allow_redirects=False, timeout=5)
        
        if response.status_code in [302, 303, 401]:
            print("✅ Protected route correctly requires authentication")
        else:
            print(f"⚠️  Protected route returned {response.status_code} (expected 302/401)")
            
    except Exception as e:
        print(f"❌ Protected route test failed: {str(e)}")
    
    # Test 3: CSRF/State validation
    print("\n📋 Test 3: Security Checks")
    print("-" * 60)
    
    try:
        # Attempt callback without state (should fail)
        response = requests.get(
            f"{app_url}/auth/google/callback?code=fake_code",
            allow_redirects=False,
            timeout=5
        )
        
        if response.status_code in [302, 400]:
            print("✅ CSRF state validation appears to be working")
        else:
            print(f"⚠️  Unexpected response for invalid state: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️  CSRF test: {str(e)}")
    
    # Print configuration summary
    print("\n📋 OAuth Configuration Summary")
    print("-" * 60)
    
    google_configured = bool(os.environ.get('GOOGLE_OAUTH_CLIENT_ID'))
    github_configured = bool(os.environ.get('GITHUB_CLIENT_ID'))
    auth_secret = bool(os.environ.get('AUTH_SECRET'))
    
    print(f"Google Client ID: {'✅ Set' if google_configured else '❌ Missing'}")
    print(f"GitHub Client ID: {'✅ Set' if github_configured else '❌ Missing'}")
    print(f"Auth Secret: {'✅ Set' if auth_secret else '❌ Missing'}")
    
    print("\n📋 cURL Examples for Testing")
    print("-" * 60)
    print(f"\n# Test protected route (should return 302/401):")
    print(f"curl -i {app_url}/profile")
    
    print(f"\n# Test OAuth login redirect:")
    print(f"curl -i {app_url}/auth/google/login")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    test_oauth_endpoints()
