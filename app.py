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
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def timeout_after(seconds):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            if time.time() - start > seconds:
                raise RequestTimeout("Request timeout")
            return result
        return wrapper
    return decorator

def create_app():
    logger.info("Starting application creation...")
    app = Flask(__name__)

    # Setup configurations
    logger.info("Setting up configurations...")
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev_key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    logger.info(f"Database URL configured: {bool(app.config['SQLALCHEMY_DATABASE_URI'])}")

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_timeout": 30,
        "connect_args": {"connect_timeout": 10}
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Session configuration
    logger.info("Configuring session...")
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

    # Initialize extensions with error handling
    try:
        logger.info("Initializing database...")
        db.init_app(app)
        with app.app_context():
            logger.info("Creating database tables...")
            db.create_all()
            logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}", exc_info=True)
        raise

    try:
        logger.info("Initializing Flask-Migrate...")
        migrate = Migrate(app, db)
    except Exception as e:
        logger.error(f"Failed to initialize Flask-Migrate: {str(e)}", exc_info=True)
        raise

    try:
        logger.info("Initializing CSRF protection...")
        csrf = CSRFProtect(app)
    except Exception as e:
        logger.error(f"Failed to initialize CSRF protection: {str(e)}", exc_info=True)
        raise

    try:
        logger.info("Initializing Session...")
        Session(app)
    except Exception as e:
        logger.error(f"Failed to initialize Session: {str(e)}", exc_info=True)
        raise

    # Setup rate limiter
    try:
        logger.info("Setting up rate limiter...")
        limiter = Limiter(
            app=app,
            key_func=get_remote_address,
            default_limits=["200 per day", "50 per hour"],
            storage_uri="memory://"
        )
    except Exception as e:
        logger.error(f"Failed to initialize rate limiter: {str(e)}", exc_info=True)
        raise

    # Setup login manager
    try:
        logger.info("Setting up login manager...")
        login_manager = LoginManager()
        login_manager.init_app(app)
        login_manager.login_view = "login"
        login_manager.login_message = "Please log in to access this page."
        login_manager.login_message_category = "info"
        login_manager.session_protection = "strong"
    except Exception as e:
        logger.error(f"Failed to initialize login manager: {str(e)}", exc_info=True)
        raise

    # Request logging
    @app.before_request
    @timeout_after(30)
    def log_request_info():
        logger.info('Request: %s %s', request.method, request.url)

    @app.after_request
    def log_response_info(response):
        logger.info('Response: %s %s %s', request.method, request.url, response.status)
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

if __name__ == "__main__":
    try:
        logger.info("Creating Flask application...")
        app = create_app()
        logger.info("Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}", exc_info=True)
        raise