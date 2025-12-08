
# Firebase Auth (Google) Setup Guide

FunList now uses Firebase Auth for Google sign-in. The frontend retrieves a Firebase ID token and posts it to `/auth/firebase/login`, where the backend verifies the token with the Firebase Admin SDK and signs the user in.

## Required configuration

Set the following environment variables (or add them to `.env`):

```
FIREBASE_ENABLED=true
FIREBASE_PROJECT_ID=your_project_id
FIREBASE_API_KEY=your_web_api_key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your_sender_id
FIREBASE_APP_ID=your_app_id
FIREBASE_CREDENTIALS_JSON=<service_account_json>  # or set FIREBASE_CREDENTIALS_PATH to a file path
SESSION_SECRET=<generate with: python -c 'import secrets; print(secrets.token_hex(32))'>
```

Notes:
- `FIREBASE_CREDENTIALS_JSON` is the easiest way to provide the service account JSON; you can also mount the file and set `FIREBASE_CREDENTIALS_PATH`.
- Google OAuth client IDs/secrets are no longer required.
- GitHub OAuth remains optional and can still be enabled via `GITHUB_CLIENT_ID`/`GITHUB_CLIENT_SECRET`.

## Quick start

1. In Firebase Console, create a project and enable the **Google** provider under *Authentication → Sign-in method*.
2. Create a Web App in Firebase to obtain the client config values (`apiKey`, `authDomain`, etc.).
3. Download a service account JSON for the project (Project Settings → Service accounts).
4. Add the environment variables above.
5. Run the app (`python main.py`) and visit `/login` → click **Continue with Google**. The browser completes Google sign-in, sends the Firebase ID token to `/auth/firebase/login`, and you’ll be redirected into the app.

## Testing and health checks

- `/login` renders the Firebase-powered Google button.
- `/_health/oauth` reports whether the required Firebase env vars are present.
- The backend will create or update users based on the Firebase UID/email and mark `email_verified` when provided by Firebase.

## Troubleshooting

- **Button disabled**: Ensure `FIREBASE_ENABLED=true` and all client config values are set.
- **Server rejects token**: Confirm the service account matches the Firebase project and that the token is issued for the same project.
- **CORS/redirect errors**: All calls are same-origin; make sure you’re testing from the app domain where the Firebase web app is allowed.
