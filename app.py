import os
import sys
import logging
import traceback
from datetime import timedelta
from flask import Flask, session, request, render_template, redirect, url_for, jsonify
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from db_init import db
from flask_migrate import Migrate
from werkzeug.exceptions import RequestTimeout
from functools import wraps
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d',
    handlers=[logging.FileHandler('app.log'),
              logging.StreamHandler()])
logger = logging.getLogger(__name__)

def create_app():
    logger.info("Starting application creation...")
    app = Flask(__name__, static_folder='static')

    # Enhanced configurations for Replit environment
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SERVER_NAME"] = None
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["GOOGLE_MAPS_API_KEY"] = "AIzaSyDRkUhORhaKILaPN0-qi9YndDShVov0DVE"

    # Database configuration
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_timeout": 30,
        "connect_args": {
            "connect_timeout": 10
        }
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Enhanced session configuration
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_USE_SIGNER'] = False
    app.config['SESSION_FILE_DIR'] = './flask_session'
    app.config['SESSION_FILE_THRESHOLD'] = 500
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
    app.config['SESSION_COOKIE_NAME'] = 'funlist_session'

    try:
        logger.info("Initializing database...")
        db.init_app(app)
        with app.app_context():
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
        raise

    try:
        logger.info("Initializing Flask-Migrate...")
        migrate = Migrate(app, db)
        logger.info("Flask-Migrate initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Flask-Migrate: {str(e)}", exc_info=True)
        raise

    try:
        logger.info("Initializing CSRF protection...")
        csrf = CSRFProtect(app)
        logger.info("CSRF protection initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize CSRF protection: {str(e)}", exc_info=True)
        raise

    try:
        logger.info("Initializing Session...")
        Session(app)
        logger.info("Session initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Session: {str(e)}", exc_info=True)
        raise

    try:
        logger.info("Setting up login manager...")
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = "login"
        login_manager.login_message = "Please log in to access this page."
        login_manager.login_message_category = "info"
        login_manager.session_protection = "strong"
        logger.info("Login manager initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize login manager: {str(e)}", exc_info=True)
        raise

    @app.before_request
    def log_request():
        logger.info(f"Incoming request: {request.method} {request.url}")
        logger.debug(f"Request headers: {dict(request.headers)}")

    @app.after_request
    def add_header(response):
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.jsdelivr.net https://*.googleapis.com https://*.cdnjs.cloudflare.com https://unpkg.com; "
            "style-src 'self' 'unsafe-inline' https://*.jsdelivr.net https://*.googleapis.com https://*.fontawesome.com https://*.cdnjs.cloudflare.com https://unpkg.com; "
            "img-src 'self' data: blob: https://*.googleapis.com https://*.gstatic.com https://*.google.com; "
            "font-src 'self' data: https://*.jsdelivr.net https://*.gstatic.com https://*.fontawesome.com https://*.bootstrapcdn.com https://*.cdnjs.cloudflare.com; "
            "connect-src 'self' https://*.googleapis.com https://*.google.com; "
            "frame-src 'self' https://*.google.com; "
            "worker-src 'self' blob:; "
        )
        response.headers['Content-Security-Policy'] = csp
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    try:
        logger.info("Importing User model...")
        from models import User
    except Exception as e:
        logger.error(f"Failed to import User model: {str(e)}", exc_info=True)
        raise

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except Exception as e:
            logger.error(f"Error loading user {user_id}: {str(e)}", exc_info=True)
            return None

    # Define a dummy get_events function for testing
    def get_events():
        return [
            {
                'id': 1,
                'title': 'Thurston County Fair',
                'description': 'A fun county fair with rides, games, and food.',
                'start_date': '2025-03-25',
                'latitude': 47.0379,
                'longitude': -122.9007,
                'category': 'Other',
                'fun_rating': 4
            },
            {
                'id': 2,
                'title': 'Olympia Music Festival',
                'description': 'Live music performances by local bands.',
                'start_date': '2025-03-26',
                'latitude': 47.0380,
                'longitude': -122.9008,
                'category': 'Music',
                'fun_rating': 5
            },
            {
                'id': 3,
                'title': 'Art Walk Downtown',
                'description': 'Explore local art galleries and street performances.',
                'start_date': '2025-03-27',
                'latitude': 47.0381,
                'longitude': -122.9009,
                'category': 'Arts',
                'fun_rating': 3
            },
            {
                'id': 4,
                'title': 'Food Truck Rally',
                'description': 'A gathering of food trucks with diverse cuisines.',
                'start_date': '2025-03-28',
                'latitude': 47.0382,
                'longitude': -122.9010,
                'category': 'Food',
                'fun_rating': 4
            },
            {
                'id': 5,
                'title': 'Soccer Tournament',
                'description': 'Local teams compete in a soccer tournament.',
                'start_date': '2025-03-29',
                'latitude': 47.0383,
                'longitude': -122.9011,
                'category': 'Sports',
                'fun_rating': 4
            },
            {
                'id': 6,
                'title': 'Farmers Market',
                'description': 'Fresh produce and handmade goods.',
                'start_date': '2025-03-30',
                'latitude': 47.0384,
                'longitude': -122.9012,
                'category': 'Other',
                'fun_rating': 3
            },
            {
                'id': 7,
                'title': 'Jazz Night',
                'description': 'An evening of jazz music at a local venue.',
                'start_date': '2025-03-31',
                'latitude': 47.0385,
                'longitude': -122.9013,
                'category': 'Music',
                'fun_rating': 5
            }
        ]

    # Add route to accept cookies
    @app.route('/accept-cookies', methods=['POST'])
    def accept_cookies():
        session['cookies_accepted'] = True
        # Return preferences to be saved client-side
        preferences = {
            'essential': True,
            'analytics': True,
            'advertising': True
        }
        return jsonify({'status': 'success', 'preferences': preferences}), 200

    # Add route to save cookie preferences
    @app.route('/save-cookie-preferences', methods=['POST'])
    def save_cookie_preferences():
        data = request.get_json()
        preferences = data.get('preferences', {})
        session['cookies_accepted'] = True
        return jsonify({'status': 'success', 'preferences': preferences}), 200

    # Add route to clear cookies for testing
    @app.route('/clear-cookies')
    def clear_cookies():
        session.pop('cookies_accepted', None)
        return redirect(url_for('map'))

    try:
        logger.info("Initializing routes...")
        # Import routes first, then initialize
        import routes
        routes.init_routes(app)
        logger.info("Routes initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize routes: {str(e)}", exc_info=True)
        raise

    # Add custom jinja filters
    @app.template_filter('tojson')
    def to_json(value):
        import json
        return json.dumps(value, default=lambda o: o.to_dict() if hasattr(o, 'to_dict') else str(o))
        
    logger.info("Application creation completed successfully")
    return app