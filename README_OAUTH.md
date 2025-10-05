
# OAuth Setup Guide for FunList.ai

This guide walks you through setting up Google and GitHub OAuth authentication for FunList.ai on Replit.

## Quick Start

### 1. Generate Auth Secret

Run this command to generate a secure secret:

```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

Copy the output and save it for step 3.

### 2. Create OAuth Applications

#### Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new project or select an existing one
3. Click "Create Credentials" → "OAuth 2.0 Client ID"
4. Configure consent screen if prompted
5. Choose "Web application" as application type
6. Add authorized redirect URIs:
   - `https://YOUR-REPLIT-DOMAIN.replit.dev/auth/google/callback`
   - `http://localhost:5000/auth/google/callback` (for local testing)
7. Save the Client ID and Client Secret

#### GitHub OAuth Setup

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click "New OAuth App"
3. Fill in the details:
   - **Application name**: FunList.ai
   - **Homepage URL**: `https://YOUR-REPLIT-DOMAIN.replit.dev`
   - **Authorization callback URL**: `https://YOUR-REPLIT-DOMAIN.replit.dev/auth/github/callback`
4. Register the application
5. Generate a new client secret
6. Save the Client ID and Client Secret

### 3. Configure Replit Secrets

In your Replit project, go to "Tools" → "Secrets" and add:

```
GOOGLE_OAUTH_CLIENT_ID=your_google_client_id
GOOGLE_OAUTH_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
AUTH_SECRET=your_generated_secret_from_step_1
```

### 4. Run Database Migration

Update the database schema to support OAuth:

```bash
python update_oauth_schema.py
```

### 5. Start the Application

```bash
python main.py
```

The console will display the exact redirect URIs you need to configure in Google and GitHub.

## Testing OAuth

### Manual Testing

1. Navigate to `/login` in your browser
2. Click "Continue with Google" or "Continue with GitHub"
3. Complete the OAuth flow
4. You should be redirected back and logged in

### Automated Testing

Run the test suite:

```bash
python test_oauth.py
```

This will verify:
- OAuth redirects are working
- Protected routes require authentication
- CSRF/state validation is active

### cURL Examples

Test protected route (should return 302 redirect or 401):
```bash
curl -i https://your-repl.replit.dev/profile
```

Test OAuth login redirect:
```bash
curl -i https://your-repl.replit.dev/auth/google/login
```

## Security Features

- ✅ **PKCE (Proof Key for Code Exchange)**: Protects against authorization code interception
- ✅ **State Parameter**: CSRF protection for OAuth flows
- ✅ **Secure Cookies**: httpOnly, secure, sameSite=Lax
- ✅ **Minimal Scopes**: Only requests email and profile information
- ✅ **Nonce Validation**: Additional security for ID tokens (Google)
- ✅ **Origin Validation**: Redirect URIs are whitelisted

## Troubleshooting

### Common Errors

**"Invalid OAuth state"**
- This is CSRF protection working correctly
- Ensure cookies are enabled
- Don't manually construct callback URLs

**"Could not retrieve email from GitHub"**
- Ensure your GitHub email is public, or
- Grant the `user:email` scope explicitly

**"Redirect URI mismatch"**
- Double-check the redirect URIs in your OAuth app settings
- Must match exactly (including http/https and trailing slashes)
- Check the console output for the exact URIs to use

**OAuth provider not configured**
- Verify all required secrets are set in Replit
- Restart the application after adding secrets

### Debug Mode

Enable detailed OAuth logging by setting:
```
OAUTHLIB_INSECURE_TRANSPORT=1  # Only for local testing!
```

## Migration to Production Database

When moving from SQLite to AlloyDB/Cloud SQL:

1. Update `DATABASE_URL` secret with new connection string
2. Run migration: `python update_oauth_schema.py`
3. Test OAuth flows in production environment
4. Update OAuth app redirect URIs to production domain

## Architecture Notes

- **OAuth Library**: Authlib (modern, supports PKCE)
- **Session Management**: Flask-Login + Flask-Session
- **Database**: PostgreSQL (current) → AlloyDB (future)
- **User Linking**: Accounts are linked by email address
- **Password-less**: OAuth users don't need passwords

## Support

For issues or questions:
- Check application logs for detailed error messages
- Review the OAuth provider's documentation
- Test with the included `test_oauth.py` script
