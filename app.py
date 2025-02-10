import os
import logging
from datetime import timedelta
from flask import Flask, session
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from db_init import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# create the app
app = Flask(__name__)

# setup configurations
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev_key")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout after 30 minutes
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)  # Remember me duration
app.config['REMEMBER_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

# initialize extensions
db.init_app(app)
csrf = CSRFProtect(app)  # Initialize CSRF protection
Session(app)  # Initialize Flask-Session

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"
login_manager.session_protection = "strong"  # Enable strong session protection

# Import models and routes after app initialization to avoid circular imports
from models import User  # noqa: E402
from routes import init_routes  # noqa: E402

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Initialize routes
init_routes(app)

# Tables are managed by update_schema.py

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
