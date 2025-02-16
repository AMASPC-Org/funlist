import os
import logging
from datetime import timedelta
from flask import Flask, session, request
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from db_init import db, init_db

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d'
)
logger = logging.getLogger(__name__)

# create the app
app = Flask(__name__)
app.config["DEBUG"] = True  # Enable debug mode

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Add request logging
@app.before_request
def log_request_info():
    logger.debug('Request: %s %s', request.method, request.url)

@app.after_request
def log_response_info(response):
    logger.debug('Response: %s %s %s', request.method, request.url, response.status)
    return response

# setup configurations
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_timeout": 30,
    "connect_args": {"connect_timeout": 10}
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True  # Log all SQL statements

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

try:
    # initialize extensions
    logger.info("Initializing Flask extensions...")
    db.init_app(app)
    csrf = CSRFProtect(app)
    Session(app)

    # Initialize database
    logger.info("Initializing database...")
    init_db(app)

    # Setup login manager
    logger.info("Setting up login manager...")
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"
    login_manager.session_protection = "strong"

    # Import models and routes after app initialization to avoid circular imports
    logger.info("Importing models and routes...")
    from models import User
    from routes import init_routes

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Initialize routes
    logger.info("Initializing routes...")
    init_routes(app)

except Exception as e:
    logger.error(f"Error during application startup: {str(e)}", exc_info=True)
    raise

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)