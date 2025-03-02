from flask import Flask
from db_init import db
import os
import logging
from sqlalchemy import Column, Boolean
from models import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def update_schema():
    app = create_app()
    with app.app_context():
        conn = db.engine.connect()
        # Check if columns exist before trying to add them
        inspector = db.inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns('user')]

        try:
            if 'is_subscriber' not in columns:
                conn.execute('ALTER TABLE user ADD COLUMN is_subscriber BOOLEAN DEFAULT 1')
                logger.info("Added is_subscriber column")

            if 'is_event_creator' not in columns:
                conn.execute('ALTER TABLE user ADD COLUMN is_event_creator BOOLEAN DEFAULT 0')
                logger.info("Added is_event_creator column")

            # All existing users should be subscribers
            conn.execute('UPDATE user SET is_subscriber = 1 WHERE is_subscriber IS NULL')

            # Make admin user have all roles
            conn.execute("UPDATE user SET is_subscriber = 1, is_event_creator = 1, is_organizer = 1 WHERE email = 'ryan@americanmarketingalliance.com'")

            logger.info("Schema update completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")
            return False
        finally:
            conn.close()

if __name__ == "__main__":
    success = update_schema()
    if success:
        print("Schema updated successfully.")
    else:
        print("Failed to update schema.")