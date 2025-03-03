
from app import create_app
from db_init import db
from models import User, Event, Subscriber, SourceWebsite
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_database_schema():
    app = create_app()
    with app.app_context():
        try:
            # Ensure reset_token and reset_token_expiry columns exist in User table
            existing_columns = [column.name for column in User.__table__.columns]
            
            if 'reset_token' not in existing_columns:
                logger.info("Adding reset_token column to User table")
                db.engine.execute('ALTER TABLE user ADD COLUMN reset_token VARCHAR(100)')
            
            if 'reset_token_expiry' not in existing_columns:
                logger.info("Adding reset_token_expiry column to User table")
                db.engine.execute('ALTER TABLE user ADD COLUMN reset_token_expiry DATETIME')
            
            logger.info("Database schema updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")
            return False

if __name__ == "__main__":
    fix_database_schema()
