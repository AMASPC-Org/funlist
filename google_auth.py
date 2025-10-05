# Use this Flask blueprint for Google authentication. Do not use flask-dance.
# Reference: flask_google_oauth integration

import json
import os
import secrets

import requests
from db_init import db
from flask import Blueprint, redirect, request, url_for, flash, session
from flask_login import login_required, login_user, logout_user
from models import User
from oauthlib.oauth2 import WebApplicationClient

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

# Make sure to use this redirect URL. It has to match the one in the whitelist
DEV_REDIRECT_URL = f'https://{os.environ.get("REPLIT_DEV_DOMAIN", "localhost")}/google_login/callback'

# Initialize client globally if configured
client = None

# Check if Google OAuth is configured
if GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET:
    client = WebApplicationClient(GOOGLE_CLIENT_ID)
    print(f"""✅ Google OAuth configured successfully!
Redirect URL: {DEV_REDIRECT_URL}
Make sure this URL is added to your Google OAuth configuration.""")
else:
    print(f"""⚠️  Google OAuth not configured. To set up:
1. Go to https://console.cloud.google.com/apis/credentials
2. Create a new OAuth 2.0 Client ID
3. Add {DEV_REDIRECT_URL} to Authorized redirect URIs
4. Add GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET to secrets""")

google_auth = Blueprint("google_auth", __name__)


@google_auth.route("/google_login")
def login():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET or not client:
        flash('Google OAuth is not configured. Please contact support.', 'error')
        return redirect(url_for('routes.login'))

    try:
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Generate and store state for CSRF protection
        state = secrets.token_urlsafe(32)
        session['oauth_state'] = state

        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            # Replacing http:// with https:// is important as the external
            # protocol must be https to match the URI whitelisted
            redirect_uri=request.base_url.replace("http://", "https://") + "/callback",
            scope=["openid", "email", "profile"],
            state=state,
        )
        return redirect(request_uri)
    except Exception as e:
        flash('Google sign-in temporarily unavailable. Please try email login.', 'error')
        return redirect(url_for('routes.login'))


@google_auth.route("/google_login/callback")
def callback():
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET or not client:
        flash('Google OAuth is not configured.', 'error')
        return redirect(url_for('routes.login'))

    try:
        # Verify state parameter for CSRF protection
        state = request.args.get("state")
        if not state or state != session.get('oauth_state'):
            flash('Invalid authentication request. Please try again.', 'error')
            return redirect(url_for('routes.login'))

        # Clear the state from session
        session.pop('oauth_state', None)

        code = request.args.get("code")
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            # Replacing http:// with https:// is important as the external
            # protocol must be https to match the URI whitelisted
            authorization_response=request.url.replace("http://", "https://"),
            redirect_url=request.base_url.replace("http://", "https://"),
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
        )

        client.parse_request_body_response(json.dumps(token_response.json()))

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        userinfo = userinfo_response.json()
        if userinfo.get("email_verified"):
            users_email = userinfo["email"]
            users_name = userinfo["given_name"]
        else:
            flash("Google account email not verified. Please use email login.", 'error')
            return redirect(url_for('routes.login'))

        user = User.query.filter_by(email=users_email).first()
        if not user:
            # Create new user from Google account
            from werkzeug.security import generate_password_hash
            user = User(
                email=users_email,
                first_name=users_name,
                last_name="",
                password_hash=generate_password_hash(os.urandom(32).hex()),  # Random password for OAuth users
                oauth_provider='google',
                oauth_provider_id=userinfo.get('sub', ''),
                email_verified=True
            )
            db.session.add(user)
            db.session.commit()
            flash(f'Welcome {users_name}! Your account has been created.', 'success')

        login_user(user)

        # Redirect to the page they were trying to access, or home
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('routes.index'))

    except Exception as e:
        flash('Google sign-in failed. Please try email login.', 'error')
        return redirect(url_for('routes.login'))


@google_auth.route("/google_logout")
@login_required
def google_logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('routes.index'))