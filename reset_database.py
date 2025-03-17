
from flask import Flask
from db_init import db
from models import User, Event, Subscriber
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_database():
    app = Flask(__name__)
    
    # Ensure the instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/funlist.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    with app.app_context():
        try:
            # Drop all tables
            db.drop_all()
            logger.info("All tables dropped successfully")
            
            # Create tables with correct schema
            db.create_all()
            logger.info("All tables recreated successfully")
            
            return True
        except Exception as e:
            logger.error(f"Error resetting database: {str(e)}")
            return False

if __name__ == "__main__":
    success = reset_database()
    if success:
        print("Database reset successfully. You can now register and login.")
    else:
        print("Failed to reset database.")
