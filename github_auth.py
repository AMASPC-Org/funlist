
import os
from flask import Blueprint, redirect, url_for, flash, session, request
from flask_login import login_user, current_user
from models import User
from db_init import db
from oauth_providers import oauth
import secrets

github_auth = Blueprint("github_auth", __name__, url_prefix='/auth/github')

@github_auth.route('/login')
def login():
    """Initiate GitHub OAuth flow with PKCE"""
    if current_user.is_authenticated:
        return redirect(url_for('routes.index'))
    
    # Generate and store PKCE code verifier
    code_verifier = secrets.token_urlsafe(64)
    session['oauth_code_verifier'] = code_verifier
    
    # Generate CSRF state token
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state
    
    # Determine redirect URI based on environment
    base_url = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')
    protocol = 'https' if 'replit.dev' in base_url else 'http'
    redirect_uri = f"{protocol}://{base_url}/auth/github/callback"
    
    if oauth and hasattr(oauth, 'github'):
        return oauth.github.authorize_redirect(
            redirect_uri,
            state=state,
            code_verifier=code_verifier
        )
    else:
        flash('GitHub OAuth is not configured.', 'error')
        return redirect(url_for('routes.login'))

@github_auth.route('/callback')
def callback():
    """Handle GitHub OAuth callback with security validation"""
    try:
        # Verify state parameter (CSRF protection)
        state = session.pop('oauth_state', None)
        if not state or state != request.args.get('state'):
            flash('Invalid OAuth state. Please try again.', 'danger')
            return redirect(url_for('routes.login'))
        
        # Get code verifier for PKCE
        code_verifier = session.pop('oauth_code_verifier', None)
        
        # Exchange authorization code for token
        if not oauth or not hasattr(oauth, 'github'):
            raise Exception("GitHub OAuth not configured")
        
        token = oauth.github.authorize_access_token(code_verifier=code_verifier)
        
        # Get user info from GitHub API
        resp = oauth.github.get('user', token=token)
        user_info = resp.json()
        
        # Get primary email (GitHub might not include it in user endpoint)
        if not user_info.get('email'):
            emails_resp = oauth.github.get('user/emails', token=token)
            emails = emails_resp.json()
            primary_email = next((e for e in emails if e.get('primary')), None)
            if primary_email:
                user_info['email'] = primary_email['email']
                user_info['email_verified'] = primary_email.get('verified', False)
        
        if not user_info.get('email'):
            flash('Could not retrieve email from GitHub. Please ensure your email is public or grant email scope.', 'danger')
            return redirect(url_for('routes.login'))
        
        # Find or create user
        user = User.query.filter_by(email=user_info['email']).first()
        
        if not user:
            # Parse name from GitHub name field
            name_parts = (user_info.get('name') or '').split(' ', 1)
            first_name = name_parts[0] if name_parts else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            # Create new user
            from werkzeug.security import generate_password_hash
            user = User(
                email=user_info['email'],
                first_name=first_name,
                last_name=last_name,
                password_hash=generate_password_hash(os.urandom(32).hex()),  # Random password for OAuth users
                oauth_provider='github',
                oauth_provider_id=str(user_info['id']),
                email_verified=user_info.get('email_verified', False)
            )
            db.session.add(user)
        else:
            # Update OAuth info for existing user
            if not user.oauth_provider:
                user.oauth_provider = 'github'
                user.oauth_provider_id = str(user_info['id'])
        
        db.session.commit()
        
        # Log the user in
        login_user(user, remember=True)
        flash(f'Successfully signed in with GitHub!', 'success')
        
        return redirect(url_for('routes.index'))
        
    except Exception as e:
        print(f"❌ GitHub OAuth error: {str(e)}")
        flash('An error occurred during GitHub sign-in. Please try again.', 'danger')
        return redirect(url_for('routes.login'))
