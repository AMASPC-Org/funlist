import atexit
import logging
import os
import sys
import traceback
import time
from datetime import datetime
from functools import wraps
from typing import Optional
from urllib.parse import urlparse

from flask import Flask, session, request, render_template, redirect, url_for, jsonify
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from werkzeug.exceptions import RequestTimeout
from markupsafe import Markup

from app_config import DatabaseConfig, load_base_config, prepare_database_config
from config import settings
from db_init import db
from session_setup import configure_sessions
from sqlalchemy.exc import IntegrityError

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d',
    handlers=[logging.FileHandler('app.log'),
              logging.StreamHandler()])
logger = logging.getLogger(__name__)

def create_app(init_db: Optional[bool] = None, seed_on_start: Optional[bool] = None, use_server_side_sessions: Optional[bool] = None):
    logger.info("Starting application creation...")
    app = Flask(__name__, static_folder='static')

    # Base config and database wiring
    load_base_config(app, logger)
    db_config: DatabaseConfig = prepare_database_config(logger)
    connector = db_config.connector

    app.config["SQLALCHEMY_DATABASE_URI"] = db_config.database_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = db_config.engine_options

    init_db_on_start = settings.get_bool("INIT_DB_ON_START", False) if init_db is None else init_db
    seed_on_boot = settings.get_bool("SEED_ON_START", False) if seed_on_start is None else seed_on_start
    server_side_sessions = True if use_server_side_sessions is None else use_server_side_sessions

    parsed_db = urlparse(db_config.database_url)
    logger.info(
        "App config resolved: init_db_on_start=%s, seed_on_start=%s, server_side_sessions=%s, db_driver=%s",
        init_db_on_start,
        seed_on_boot,
        server_side_sessions,
        parsed_db.scheme,
    )
    logger.debug("Engine options: %s", db_config.engine_options)

    configure_sessions(app, db, use_server_side=server_side_sessions)
    logger.debug(
        "Session settings: type=%s, cookie_name=%s, secure=%s, lifetime=%s",
        app.config.get("SESSION_TYPE"),
        app.config.get("SESSION_COOKIE_NAME"),
        app.config.get("SESSION_COOKIE_SECURE"),
        app.config.get("PERMANENT_SESSION_LIFETIME"),
    )

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
        if init_db_on_start:
            with app.app_context():
                try:
                    drop_and_recreate = settings.get_bool("DROP_AND_RECREATE_DB", False) or os.environ.get("DROP_AND_RECREATE_DB") in {"1", "true", "True"}
                    if drop_and_recreate:
                        logger.warning("DROP_AND_RECREATE_DB enabled: dropping all tables before recreate.")
                        db.drop_all()
                        db.session.commit()

                    logger.info("Creating all tables...")
                    db.create_all()
                    logger.info("Database tables created successfully")

                    if seed_on_boot:
                        try:
                            logger.info("Starting seed-on-start")
                            from seed import seed as run_seed

                            seed_result = run_seed(app) or {}
                            logger.info(
                                "Seed-on-start completed: %s chapters, %s events",
                                seed_result.get("chapters"),
                                seed_result.get("events"),
                            )
                        except Exception as seed_error:  # noqa: BLE001
                            logger.error(
                                "Seed-on-start failed: %s", seed_error, exc_info=True
                            )
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
        else:
            logger.info("Database creation and seeding skipped (init_db_on_start=False)")
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

    # Firebase client configuration for frontend auth
    firebase_client_config = {
        "apiKey": settings.get("FIREBASE_API_KEY"),
        "authDomain": settings.get("FIREBASE_AUTH_DOMAIN"),
        "projectId": settings.get("FIREBASE_PROJECT_ID"),
        "storageBucket": settings.get("FIREBASE_STORAGE_BUCKET"),
        "messagingSenderId": settings.get("FIREBASE_MESSAGING_SENDER_ID"),
        "appId": settings.get("FIREBASE_APP_ID"),
    }
    firebase_client_config = {k: v for k, v in firebase_client_config.items() if v}
    firebase_enabled = settings.get_bool("FIREBASE_ENABLED", False) and bool(firebase_client_config)
    app.config["FIREBASE_CLIENT_CONFIG"] = firebase_client_config
    app.config["FIREBASE_ENABLED"] = firebase_enabled

    if firebase_enabled:
        try:
            from firebase_auth import init_firebase_app
            init_firebase_app(logger=logger)
            logger.info("Firebase auth initialized successfully")
        except Exception as e:
            logger.error("Firebase auth enabled but initialization failed: %s", e, exc_info=True)
            firebase_enabled = False
            app.config["FIREBASE_ENABLED"] = False

    logger.info("Session configuration applied (server_side_sessions=%s)", server_side_sessions)

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
        # Skip noisy static/health traffic to keep log volume and I/O overhead low
        path = request.path or ""
        if path.startswith("/static") or path == "/favicon.ico":
            return
        if request.method == 'HEAD' and path == '/api':
            return
        logger.info(f"Incoming request: {request.method} {request.url}")
        logger.debug(f"Request headers: {dict(request.headers)}")

    @app.after_request
    def add_header(response):
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://*.jsdelivr.net https://maps.googleapis.com https://*.googleapis.com https://*.cdnjs.cloudflare.com https://unpkg.com https://www.gstatic.com https://www.gstatic.com/firebasejs https://apis.google.com https://*.firebaseapp.com; "
            "style-src 'self' 'unsafe-inline' https://*.jsdelivr.net https://*.googleapis.com https://*.fontawesome.com https://*.cdnjs.cloudflare.com https://unpkg.com; "
            "img-src 'self' data: blob: https://*.googleapis.com https://*.gstatic.com https://*.google.com https://firebasestorage.googleapis.com; "
            "font-src 'self' data: https://*.jsdelivr.net https://*.gstatic.com https://*.fontawesome.com https://*.bootstrapcdn.com https://*.cdnjs.cloudflare.com; "
            "connect-src 'self' https://unpkg.com https://*.googleapis.com https://*.google.com https://maps.googleapis.com https://securetoken.googleapis.com https://identitytoolkit.googleapis.com https://firebaseinstallations.googleapis.com https://*.firebaseapp.com https://www.gstatic.com https://www.google-analytics.com https://www.googletagmanager.com https://*.jsdelivr.net; "
            "frame-src 'self' https://*.google.com https://*.firebaseapp.com https://accounts.google.com; "
            "worker-src 'self' blob:; "
        )
        response.headers['Content-Security-Policy'] = csp
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-CSRFToken, X-CSRF-Token'
        return response

    @login_manager.user_loader
    def load_user(user_id):
        try:
            return db.session.get(User, int(user_id))
        except Exception as e:
            logger.error(f"Error loading user {user_id}: {str(e)}", exc_info=True)
            return None

    if connector:
        def _close_cloud_sql_connector():
            try:
                connector.close()
                logger.info("Cloud SQL connector closed during shutdown")
            except Exception as connector_error:
                logger.warning("Error closing Cloud SQL connector during shutdown: %s", connector_error)

        # Close the connector once when the process exits instead of after every request
        atexit.register(_close_cloud_sql_connector)


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
        
        # Register Firebase auth blueprint
        from firebase_auth import firebase_auth_bp
        app.register_blueprint(firebase_auth_bp)
        logger.info("Firebase auth blueprint registered successfully")
        
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
        return Markup(json.dumps(value, default=lambda o: o.to_dict() if hasattr(o, 'to_dict') else str(o)))
    
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

    @app.context_processor
    def inject_firebase_config():
        return {
            "firebase_enabled": app.config.get("FIREBASE_ENABLED", False),
            "firebase_client_config": app.config.get("FIREBASE_CLIENT_CONFIG", {}),
        }
        
    logger.info("Application creation completed successfully")
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
