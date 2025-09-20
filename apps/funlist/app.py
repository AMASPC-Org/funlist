from flask import Flask, render_template, jsonify, request, session
from flask_session import Session
import os
import logging
import time
from datetime import timedelta

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a directory for session files if it doesn't exist
session_dir = os.path.join(os.path.dirname(__file__), 'sessions')
os.makedirs(session_dir, exist_ok=True)

app = Flask(__name__)

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True  # Make sessions permanent
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_FILE_DIR'] = session_dir
app.config['SESSION_FILE_THRESHOLD'] = 500
app.config['SESSION_FILE_MODE'] = 0o600
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)  # 1 month

# Initialize session
Session(app)

# Placeholder for CSRF token generation (in a real app, use Flask-WTF or similar)
# For demonstration, we'll simulate it in the template
# In a real application, you would generate and inject a CSRF token here.
# Example:
# from flask_wtf.csrf import generate_csrf
# @app.before_request
# def add_csrf_token():
#     if 'csrf_token' not in session:
#         session['csrf_token'] = generate_csrf()

@app.route('/')
def index():
    # Check if cookies have been accepted
    cookies_accepted = session.get('cookies_accepted', False)
    logger.info(f"Index page loaded. Cookies accepted: {cookies_accepted}. Session ID: {session.get('_id', 'unknown')}")
    # In a real app, you'd pass the CSRF token to the template
    # csrf_token = session.get('csrf_token')
    return render_template('index.html', cookies_accepted=cookies_accepted)

@app.route('/preferences')
def preferences():
    cookies_accepted = session.get('cookies_accepted', False)
    cookie_preferences = session.get('cookie_preferences', {})
    logger.info(f"Preferences page loaded. Cookies accepted: {cookies_accepted}. Preferences: {cookie_preferences}. Session ID: {session.get('_id', 'unknown')}")
    # In a real app, you'd pass the CSRF token to the template
    # csrf_token = session.get('csrf_token')
    return render_template('preferences.html', cookies_accepted=cookies_accepted, cookie_preferences=cookie_preferences)

@app.route('/accept-cookies', methods=['POST'])
def accept_cookies():
    try:
        # Mark cookies as accepted in session
        session['cookies_accepted'] = True
        session['cookie_timestamp'] = time.time()
        session.permanent = True  # Ensure session persists

        preferences = {
            'essential': True,
            'analytics': True,
            'advertising': True
        }

        session['cookie_preferences'] = preferences

        logger.info(f"Cookies accepted via server route. Session ID: {session.get('_id', 'unknown')}")
        return jsonify({'status': 'success', 'preferences': preferences}), 200

    except Exception as e:
        logger.error(f"Error in accept_cookies route: {str(e)}", exc_info=True)
        return jsonify({'status': 'error', 'message': 'Failed to accept cookies'}), 500

@app.route('/reject-cookies', methods=['POST'])
def reject_cookies():
    try:
        session['cookies_accepted'] = False
        session['cookie_timestamp'] = time.time()
        session.permanent = True

        preferences = {
            'essential': True,
            'analytics': False,
            'advertising': False
        }
        session['cookie_preferences'] = preferences

        logger.info(f"Cookies rejected via server route. Session ID: {session.get('_id', 'unknown')}")
        return jsonify({'status': 'success', 'preferences': preferences}), 200

    except Exception as e:
        logger.error(f"Error in reject_cookies route: {str(e)}", exc_info=True)
        return jsonify({'status': 'error', 'message': 'Failed to reject cookies'}), 500

# Placeholder for a route that might use cookies
@app.route('/data')
def get_data():
    if not session.get('cookies_accepted', False):
        logger.warning(f"Access to /data denied, cookies not accepted. Session ID: {session.get('_id', 'unknown')}")
        return jsonify({'status': 'error', 'message': 'Cookie consent required'}), 403
    # Simulate fetching data based on preferences
    preferences = session.get('cookie_preferences', {})
    logger.info(f"Access to /data granted. Session ID: {session.get('_id', 'unknown')}")
    return jsonify({
        'message': 'Here is your data!',
        'preferences': preferences,
        'session_id': session.get('_id', 'unknown')
    })

if __name__ == '__main__':
    # In a production environment, use a more robust WSGI server
    # For development, we can run the app directly
    # The CSRF token handling should be properly implemented here for a real app
    app.run(debug=True)