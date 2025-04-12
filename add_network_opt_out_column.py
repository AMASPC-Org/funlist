
import logging
from flask import Flask
from db_init import db
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_network_opt_out_column():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/funlist.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    with app.app_context():
        try:
            # Check if network_opt_out column exists
            column_exists = False
            try:
                db.session.execute(text("SELECT network_opt_out FROM events LIMIT 1"))
                column_exists = True
            except Exception:
                column_exists = False
            
            if not column_exists:
                logger.info("Adding missing network_opt_out column to events table")
                db.session.execute(text("ALTER TABLE events ADD COLUMN network_opt_out BOOLEAN DEFAULT FALSE"))
                db.session.commit()
                logger.info("Added network_opt_out column successfully")
            else:
                logger.info("network_opt_out column already exists")
                
            return True
        except Exception as e:
            logger.error(f"Error adding network_opt_out column: {str(e)}")
            return False

if __name__ == "__main__":
    success = add_network_opt_out_column()
    if success:
        print("Database schema updated successfully.")
    else:
        print("Failed to update database schema.")
