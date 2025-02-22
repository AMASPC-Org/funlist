import os
import logging
from datetime import timedelta
from flask import Flask, session, request, render_template
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

    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com https://auth.util.repl.co; style-src 'self' 'unsafe-inline' https://unpkg.com; img-src 'self' data: https://*; font-src 'self' data:; connect-src 'self' https://*;"
        return response

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

    # Session configuration
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['SESSION_COOKIE_SECURE'] = True  # Enable for HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Add request logging
    @app.before_request
    def log_request():
        logger.info(f"Incoming request: {request.method} {request.url}")
        logger.debug(f"Request headers: {dict(request.headers)}")

    @app.after_request
    def log_response(response):
        logger.info(f"Response status: {response.status}")
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
        Migrate(app, db)
    except Exception as e:
        logger.error(f"Failed to initialize Flask-Migrate: {str(e)}",
                     exc_info=True)
        raise

    try:
        logger.info("Initializing CSRF protection and rate limiting...")
        CSRFProtect(app)
        limiter = Limiter(
            app=app,
            storage_uri="memory://",
            default_limits=["200 per day", "50 per hour"],
            key_func=get_remote_address
        )

        @app.route("/login", methods=["POST"])
        @limiter.limit("5 per minute")
        def rate_limited_login():
            return "rate limited"

        @app.route("/signup", methods=["POST"])
        @limiter.limit("3 per minute")
        def rate_limited_signup():
            return "rate limited"
    except Exception as e:
        logger.error(f"Failed to initialize security measures: {str(e)}",
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

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')

    @app.route('/terms')
    def terms():
        return render_template('terms.html')

    logger.info("Application creation completed successfully")
    return app


# No app.run() or port handling here!