
from flask import Flask
from db_init import db
import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_database_schema():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///instance/funlist.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    with app.app_context():
        try:
            # Check if is_featured column exists
            column_exists = False
            try:
                db.session.execute(text("SELECT is_featured FROM events LIMIT 1"))
                column_exists = True
            except Exception:
                column_exists = False
            
            if not column_exists:
                logger.info("Adding missing is_featured column to events table")
                db.session.execute(text("ALTER TABLE events ADD COLUMN is_featured BOOLEAN DEFAULT FALSE"))
                db.session.commit()
                logger.info("Added is_featured column successfully")
            else:
                logger.info("is_featured column already exists")
                
            return True
        except Exception as e:
            logger.error(f"Error fixing database schema: {str(e)}")
            return False

if __name__ == "__main__":
    success = fix_database_schema()
    if success:
        print("Database schema fixed successfully.")
    else:
        print("Failed to fix database schema.")
