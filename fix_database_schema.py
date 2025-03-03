
from app import create_app
from models import User, Event, Subscriber
from db_init import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_database_schema():
    app = create_app()
    with app.app_context():
        try:
            # Check for reset_token and reset_token_expiry columns
            # If they don't exist, add them
            if 'reset_token' not in [column.name for column in User.__table__.columns]:
                logger.info("Adding reset_token column to User table")
                db.engine.execute('ALTER TABLE user ADD COLUMN reset_token VARCHAR(100);')
            
            if 'reset_token_expiry' not in [column.name for column in User.__table__.columns]:
                logger.info("Adding reset_token_expiry column to User table")
                db.engine.execute('ALTER TABLE user ADD COLUMN reset_token_expiry DATETIME;')
            
            # Add more schema fixes as needed
            
            logger.info("Database schema update completed successfully")
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")

if __name__ == "__main__":
    fix_database_schema()
