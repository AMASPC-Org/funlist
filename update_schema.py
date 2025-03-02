
from flask import Flask
from db_init import db
import os
import logging
from sqlalchemy import text

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
        try:
            # Check existing columns
            inspector = db.inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('user')]
            
            # Add new columns if they don't exist
            with db.engine.connect() as conn:
                if 'is_subscriber' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN is_subscriber BOOLEAN DEFAULT TRUE'))
                    conn.commit()
                    logger.info("Added is_subscriber column")
                
                if 'is_event_creator' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN is_event_creator BOOLEAN DEFAULT FALSE'))
                    conn.commit()
                    logger.info("Added is_event_creator column")
                
                # Update existing users
                conn.execute(text('UPDATE "user" SET is_subscriber = TRUE WHERE is_subscriber IS NULL'))
                conn.commit()
                
                # Update admin user
                conn.execute(text("UPDATE \"user\" SET is_subscriber = TRUE, is_event_creator = TRUE, is_organizer = TRUE WHERE email = 'ryan@americanmarketingalliance.com'"))
                conn.commit()
                
            logger.info("Schema update completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")
            return False

if __name__ == "__main__":
    success = update_schema()
    if success:
        print("Schema updated successfully.")
    else:
        print("Failed to update schema.")
