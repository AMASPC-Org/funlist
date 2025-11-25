import os
import sys
import logging
import traceback
from datetime import timedelta, datetime
from flask import Flask, session, request, render_template, redirect, url_for, jsonify
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from db_init import db
from flask_migrate import Migrate
from werkzeug.exceptions import RequestTimeout
from functools import wraps
import time

from config import settings
from sqlalchemy.exc import IntegrityError

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

    # Production configurations
    app.config["SECRET_KEY"] = os.environ.get("SESSION_SECRET")
    if not app.config["SECRET_KEY"]:
        raise ValueError("SESSION_SECRET environment variable must be set")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.get("DATABASE_URL")
    if not app.config["SQLALCHEMY_DATABASE_URI"]:
        raise ValueError("DATABASE_URL environment variable must be set")
    
    app.config["SERVER_NAME"] = None
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "https"
    
    app.config["GOOGLE_MAPS_API_KEY"] = settings.get("GOOGLE_MAPS_API_KEY", required=True)
    if not app.config["GOOGLE_MAPS_API_KEY"]:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable must be set")

    # Default map bounds (fallback to WA/PNW region). Values can be overridden via env.
    def _get_float(key: str, default: float) -> float:
        try:
            value = settings.get(key)
            return float(value) if value else default
        except (TypeError, ValueError):
            return float(default)

    app.config["MAP_BOUNDS_NORTH"] = _get_float("MAP_BOUNDS_NORTH", 49.0)
    app.config["MAP_BOUNDS_SOUTH"] = _get_float("MAP_BOUNDS_SOUTH", 45.5)
    app.config["MAP_BOUNDS_WEST"] = _get_float("MAP_BOUNDS_WEST", -124.8)
    app.config["MAP_BOUNDS_EAST"] = _get_float("MAP_BOUNDS_EAST", -116.9)

    # Database configuration
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_timeout": 30
    }

    # Simple session configuration using Flask's default signed cookie sessions
    secure_session_cookie = settings.get_bool("SESSION_COOKIE_SECURE", True)
    if os.environ.get('PROD'):
        secure_session_cookie = True
    app.config['SESSION_COOKIE_SECURE'] = secure_session_cookie
    app.config['SESSION_COOKIE_NAME'] = '__Host-funlist' if secure_session_cookie else 'funlist_session'

    # Production session configuration (database-backed for Cloud Run)
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'flask_sessions'  # Use unique table name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    try:
        logger.info("Importing models...")
        import models  # noqa: F401 (imported for side effects)
        User = models.User  # Used by login manager below
    except Exception as e:
        logger.error(f"Failed to import models: {str(e)}", exc_info=True)
        raise

    try:
        logger.info("Initializing database...")
        db.init_app(app)
        with app.app_context():
            try:
                db.create_all()
                logger.info("Database tables created successfully")
            except IntegrityError as integrity_error:
                db.session.rollback()
                error_text = str(integrity_error)
                if "pg_type_typname_nsp_index" in error_text or "already exists" in error_text:
                    logger.warning(
                        "Database already had required tables/types. "
                        "Continuing startup after IntegrityError: %s",
                        error_text
                    )
                else:
                    raise
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

    # Using Flask's default signed cookie sessions - no additional session extension needed
    logger.info("Using Flask default signed cookie sessions")

    try:
        logger.info("Setting up login manager...")
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = "login"  # type: ignore
        login_manager.login_message = "Please log in to access this page."
        login_manager.login_message_category = "info"
        login_manager.session_protection = "strong"
        logger.info("Login manager initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize login manager: {str(e)}", exc_info=True)
        raise

    @app.before_request
    def log_request():
        # Don't log HEAD requests to /api (health checks) to reduce log noise
        if not (request.method == 'HEAD' and request.path == '/api'):
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

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except Exception as e:
            logger.error(f"Error loading user {user_id}: {str(e)}", exc_info=True)
            return None


    # Add route to accept cookies
    @app.route('/accept-cookies', methods=['POST'])
    def accept_cookies():
        try:
            session['cookies_accepted'] = True
            # Return preferences to be saved client-side
            preferences = {
                'essential': True,
                'analytics': True,
                'advertising': True
            }
            return jsonify({'status': 'success', 'preferences': preferences}), 200
        except Exception as e:
            logger.error(f"Error accepting cookies: {str(e)}")
            return jsonify({'status': 'error', 'message': 'Failed to accept cookies'}), 500

    # Add CSRF exempt route for cookie acceptance (fallback)
    @app.route('/accept-cookies-simple', methods=['POST'])
    @csrf.exempt
    def accept_cookies_simple():
        try:
            session['cookies_accepted'] = True
            preferences = {
                'essential': True,
                'analytics': True,
                'advertising': True
            }
            return jsonify({'status': 'success', 'preferences': preferences}), 200
        except Exception as e:
            logger.error(f"Error accepting cookies: {str(e)}")
            return jsonify({'status': 'error', 'message': 'Failed to accept cookies'}), 500

    # Add route to save cookie preferences
    @app.route('/save-cookie-preferences', methods=['POST'])
    def save_cookie_preferences():
        try:
            data = request.get_json() or {}
            preferences = data.get('preferences', {})
            session['cookies_accepted'] = True
            return jsonify({'status': 'success', 'preferences': preferences}), 200
        except Exception as e:
            logger.error(f"Error saving cookie preferences: {str(e)}")
            return jsonify({'status': 'error', 'message': 'Failed to save preferences'}), 500

    # Add route to clear cookies for testing
    @app.route('/clear-cookies')
    def clear_cookies():
        session.pop('cookies_accepted', None)
        return redirect(url_for('map'))

    try:
        logger.info("Initializing OAuth providers...")
        from oauth_providers import init_oauth
        oauth = init_oauth(app)
        logger.info("OAuth providers initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize OAuth providers: {str(e)}", exc_info=True)
        raise
    
    try:
        logger.info("Initializing routes...")
        # Import routes first, then initialize
        import routes
        routes.init_routes(app)
        
        # Register debug routes for OAuth health checks
        from routes_debug import debug
        app.register_blueprint(debug)
        
        # Register AI routes blueprint
        from routes_ai import ai_routes
        app.register_blueprint(ai_routes)
        logger.info("AI routes registered successfully")
        
        logger.info("Routes initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize routes: {str(e)}", exc_info=True)
        raise

    # Add custom jinja filters
    @app.template_filter('tojson')
    def to_json(value):
        import json
        return json.dumps(value, default=lambda o: o.to_dict() if hasattr(o, 'to_dict') else str(o))
    
    @app.template_filter('format_datetime')
    def format_datetime(value, fmt='%B %d, %Y'):
        """Format datetime or ISO strings gracefully in templates."""
        if not value:
            return 'TBA'
        if hasattr(value, 'strftime'):
            return value.strftime(fmt)
        if isinstance(value, str):
            for date_format in ('%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d'):
                try:
                    parsed = datetime.strptime(value, date_format)
                    return parsed.strftime(fmt)
                except ValueError:
                    continue
            try:
                parsed = datetime.fromisoformat(value)
                return parsed.strftime(fmt)
            except ValueError:
                return value
        return str(value)
    
    @app.template_filter('format_time')
    def format_time(value, fmt='%I:%M %p'):
        """Format time objects or HH:MM strings without errors."""
        if not value:
            return ''
        if hasattr(value, 'strftime'):
            return value.strftime(fmt)
        if isinstance(value, str):
            for time_format in ('%H:%M:%S', '%H:%M'):
                try:
                    parsed = datetime.strptime(value, time_format)
                    return parsed.strftime(fmt)
                except ValueError:
                    continue
        return str(value)
        
    logger.info("Application creation completed successfully")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
