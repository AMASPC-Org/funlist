
from db_init import db
import logging
from models import User, Event, SourceWebsite, Subscriber
from sqlalchemy import inspect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    inspector = inspect(db.engine)
    columns = inspector.get_columns(table_name)
    return any(col['name'] == column_name for col in columns)

def add_missing_columns():
    """Add missing columns to the database"""
    try:
        # Check and add reset_token column
        if not check_column_exists('user', 'reset_token'):
            logger.info("Adding reset_token column to user table")
            db.engine.execute('ALTER TABLE "user" ADD COLUMN reset_token VARCHAR(100)')
            
        # Check and add reset_token_expiry column
        if not check_column_exists('user', 'reset_token_expiry'):
            logger.info("Adding reset_token_expiry column to user table")
            db.engine.execute('ALTER TABLE "user" ADD COLUMN reset_token_expiry TIMESTAMP')
            
        logger.info("Schema update completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error updating schema: {e}")
        return False

if __name__ == "__main__":
    add_missing_columns()
