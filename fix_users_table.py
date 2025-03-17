
import logging
from sqlalchemy import inspect, text
from db_init import db
from app import create_app
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_users_table():
    """Create or fix the users table to match current models"""
    app = create_app()
    
    with app.app_context():
        # Ensure the instance directory exists
        os.makedirs('instance', exist_ok=True)
        
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        # Check if users table exists
        if 'users' not in tables:
            logger.info("Users table doesn't exist. Creating all tables...")
            db.create_all()
            logger.info("Tables created successfully.")
            return True
        
        # If users table exists, check and add missing columns
        columns = [column['name'] for column in inspector.get_columns('users')]
        logger.info(f"Existing columns in users table: {columns}")
        
        # Define required columns
        required_columns = [
            ('is_event_creator', 'BOOLEAN DEFAULT FALSE'), 
            ('is_organizer', 'BOOLEAN DEFAULT FALSE'),
            ('is_vendor', 'BOOLEAN DEFAULT FALSE'),
            ('vendor_type', 'VARCHAR(50)'),
            ('vendor_description', 'TEXT'),
            ('vendor_profile_updated_at', 'TIMESTAMP'),
            ('company_name', 'VARCHAR(100)'),
            ('organizer_description', 'TEXT'),
            ('organizer_website', 'VARCHAR(200)'),
            ('advertising_opportunities', 'TEXT'),
            ('sponsorship_opportunities', 'TEXT'),
            ('organizer_profile_updated_at', 'TIMESTAMP'),
            ('bio', 'TEXT'),
            ('location', 'VARCHAR(200)'),
            ('phone', 'VARCHAR(20)'),
            ('newsletter_opt_in', 'BOOLEAN DEFAULT TRUE'),
            ('marketing_opt_in', 'BOOLEAN DEFAULT FALSE'),
            ('user_preferences', 'TEXT'),
            ('birth_date', 'TIMESTAMP'),
            ('interests', 'TEXT')
        ]
        
        # Add missing columns
        for col_name, col_type in required_columns:
            if col_name not in columns:
                try:
                    logger.info(f"Adding column {col_name} to users table...")
                    db.session.execute(text(f"ALTER TABLE users ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                    logger.info(f"Column {col_name} added successfully.")
                except Exception as e:
                    logger.error(f"Error adding column {col_name}: {str(e)}")
        
        db.session.commit()
        logger.info("Users table schema update completed")
        return True

if __name__ == "__main__":
    success = fix_users_table()
    if success:
        print("Users table schema fixed successfully.")
    else:
        print("Failed to fix users table schema.")
