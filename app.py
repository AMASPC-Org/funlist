import os
import logging
from flask import Flask
from flask_login import LoginManager
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

# initialize extensions
db.init_app(app)

# Setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # type: ignore

# Import models and routes after app initialization to avoid circular imports
from models import User  # noqa: E402
from routes import init_routes  # noqa: E402

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Initialize routes
init_routes(app)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
