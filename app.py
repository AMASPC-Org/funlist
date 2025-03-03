import os
import logging
from datetime import timedelta
from flask import Flask, session, request
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from db_init import db
from flask_migrate import Migrate
from werkzeug.exceptions import RequestTimeout
from functools import wraps
import time

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format=
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d',
    handlers=[logging.FileHandler('app.log'),
              logging.StreamHandler()])
logger = logging.getLogger(__name__)


def create_app():
    logger.info("Starting application creation...")
    app = Flask(__name__, static_folder='static')

    # Enhanced configurations for Replit environment
    app.config["SECRET_KEY"] = os.environ.get(
        "FLASK_SECRET_KEY", "dev_key")  # Use environment variable
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SERVER_NAME"] = None  # Allow all hostnames
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "https"  # Added for Replit HTTPS

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

    # Simplified session configuration to fix cookie encoding issue
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    app.config['SESSION_COOKIE_SECURE'] = False  # Disable for local development
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_USE_SIGNER'] = False  # Disable signer which can cause encoding issues
    app.config['SESSION_FILE_DIR'] = './flask_session'
    
    # Initialize Flask-Session
    from flask_session import Session
    Session(app)
    
    # Clear existing session files to start fresh
    for f in os.listdir('./flask_session'):
        if f != '.gitkeep':
            os.remove(os.path.join('./flask_session', f))

    # Add request logging
    @app.before_request
    def log_request():
        logger.info(f"Incoming request: {request.method} {request.url}")
        logger.debug(f"Request headers: {dict(request.headers)}")

    @app.after_request
    def after_request(response):
        """Add security headers and log response details after each request."""
        # Set Content Security Policy header with more permissive options
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval' https: https://cdn.jsdelivr.net https://unpkg.com https://code.jquery.com https://auth.util.repl.co https://*.replit.dev https://*.repl.co; "
            "style-src 'self' 'unsafe-inline' https: https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "img-src 'self' data: https:; "
            "font-src 'self' data: https: https://cdnjs.cloudflare.com; "
            "connect-src 'self' https:; "
            "frame-src 'self' https: https://auth.util.repl.co https://*.replit.dev https://*.repl.co; "
            "report-uri /csp-report"
        )
        response.headers['Content-Security-Policy'] = csp

        # Log response details
        app.logger.info(f'Response status: {response.status}')
        return response

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
        logger.error(f"Failed to initialize Flask-Migrate: {str(e)}",
                     exc_info=True)
        raise

    try:
        logger.info("Initializing CSRF protection...")
        csrf = CSRFProtect(app)

        # Exempt API routes from CSRF protection
        @csrf.exempt
        def csrf_exempt_api():
            # Exempt all routes that are API routes
            if request.path.startswith('/admin/event/') and request.method == 'POST':
                return True
            return False
    except Exception as e:
        logger.error(f"Failed to initialize CSRF protection: {str(e)}",
                     exc_info=True)
        raise

    try:
        logger.info("Initializing Session...")
        Session(app)
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
    except Exception as e:
        logger.error(f"Failed to initialize login manager: {str(e)}",
                     exc_info=True)
        raise

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
            logger.error(f"Error loading user {user_id}: {str(e)}",
                         exc_info=True)
            return None

    try:
        logger.info("Initializing routes...")
        from routes import init_routes
        init_routes(app)
        logger.info("Routes initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize routes: {str(e)}", exc_info=True)
        raise

    logger.info("Application creation completed successfully")
    return app


# No app.run() or port handling here!