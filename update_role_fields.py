import os
import sys
import logging
from sqlalchemy import Column, Boolean, DateTime, text
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def update_role_fields():
    """Add new role tracking fields to the users table if they don't exist."""
    try:
        from app import db
        from sqlalchemy import inspect
        
        inspector = inspect(db.engine)
        columns = {column['name'] for column in inspector.get_columns('users')}
        
        # List of columns to check and add if they don't exist
        new_columns = {
            'roles_last_updated': 'DateTime',
            'is_event_creator_last_known': 'Boolean',
            'is_organizer_last_known': 'Boolean',
            'is_vendor_last_known': 'Boolean', 
            'is_sponsor_last_known': 'Boolean',
            'is_sponsor': 'Boolean',
            'is_subscriber': 'Boolean',
            'facebook_url': 'String',
            'instagram_url': 'String',
            'twitter_url': 'String',
            'linkedin_url': 'String',
            'tiktok_url': 'String',
            'business_phone': 'String',
            'business_email': 'String'
        }
        
        # Check and add missing columns
        added_columns = []
        for column_name, column_type in new_columns.items():
            if column_name not in columns:
                sql_statement = ""
                if column_type == 'Boolean':
                    sql_statement = f'ALTER TABLE users ADD COLUMN {column_name} BOOLEAN DEFAULT FALSE'
                elif column_type == 'DateTime':
                    sql_statement = f'ALTER TABLE users ADD COLUMN {column_name} TIMESTAMP'
                else:  # String type
                    sql_statement = f'ALTER TABLE users ADD COLUMN {column_name} VARCHAR(255)'
                
                with db.engine.connect() as connection:
                    connection.execute(text(sql_statement))
                added_columns.append(column_name)
        
        if added_columns:
            logger.info(f"Added the following columns to the users table: {', '.join(added_columns)}")
        else:
            logger.info("All required columns already exist in the users table")
        
        return True
    except SQLAlchemyError as e:
        logger.error(f"SQL error updating role fields: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error updating role fields: {str(e)}")
        return False

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        update_role_fields()
