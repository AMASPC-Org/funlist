
import os
from authlib.integrations.flask_client import OAuth

oauth = OAuth()

def init_oauth(app):
    """Initialize OAuth providers with secure configuration"""
    oauth.init_app(app)
    
    # GitHub OAuth with PKCE
    oauth.register(
        name='github',
        client_id=os.environ.get('GITHUB_CLIENT_ID'),
        client_secret=os.environ.get('GITHUB_CLIENT_SECRET'),
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        api_base_url='https://api.github.com/',
        client_kwargs={
            'scope': 'user:email',
            'code_challenge_method': 'S256'  # Enable PKCE
        }
    )
    
    # Print OAuth configuration on startup
    github_configured = bool(os.environ.get('GITHUB_CLIENT_ID'))
    
    print("\n" + "="*60)
    print("OAuth Configuration Status:")
    print("="*60)
    print(f"GitHub OAuth: {'✅ Configured' if github_configured else '❌ Not configured'}")
    
    if github_configured:
        base_url = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')
        protocol = 'https' if 'replit.dev' in base_url else 'http'
        
        print("\n📋 OAuth Redirect URIs (paste these in provider consoles):")
        print("-" * 60)
        
        if github_configured:
            print(f"\n⚫ GitHub OAuth App:")
            print(f"   {protocol}://{base_url}/auth/github/callback")
            print(f"   http://localhost:5000/auth/github/callback  (for local dev)")
        
        print("\n" + "="*60 + "\n")
    else:
        print("\n⚠️  To enable OAuth, add these secrets in Replit:")
        print("   - GITHUB_CLIENT_ID")
        print("   - GITHUB_CLIENT_SECRET")
        print("   - AUTH_SECRET (generate with: python -c 'import secrets; print(secrets.token_hex(32))')")
        print("="*60 + "\n")
    
    return oauth
