import os
import logging
from datetime import timedelta
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
from flask import session, request
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from db_init import db
from flask_migrate import Migrate  # Import Migrate

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d'
)
logger = logging.getLogger(__name__)

# create the app
app = Flask(__name__)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Add request logging
from functools import wraps
from werkzeug.exceptions import RequestTimeout
import time

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

@app.before_request
@timeout_after(30)
def log_request_info():
    logger.info('Request: %s %s', request.method, request.url)

@app.after_request
def log_response_info(response):
    logger.info('Response: %s %s %s', request.method, request.url, response.status)
    return response

# setup configurations
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///funlist.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_timeout": 30,
    "connect_args": {"connect_timeout": 10}
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

# initialize extensions
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Migrate
csrf = CSRFProtect(app)
Session(app)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"

# Import models and routes after app initialization to avoid circular imports
from models import User
from routes import init_routes

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Initialize routes
init_routes(app)

# Port configuration moved to main.py