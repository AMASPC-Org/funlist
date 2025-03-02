
from db_init import db
from models import User
import logging
from sqlalchemy import inspect

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute(f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {column_type}')

def update_schema():
    try:
        # Get database inspector
        inspector = inspect(db.engine)
        
        # Check if User table exists
        if 'user' in inspector.get_table_names():
            # Get existing columns
            columns = [col['name'] for col in inspector.get_columns('user')]
            
            # Check for missing organizer columns
            missing_columns = []
            if 'is_organizer' not in columns:
                missing_columns.append('is_organizer')
            if 'company_name' not in columns:
                missing_columns.append('company_name')
            if 'organizer_description' not in columns:
                missing_columns.append('organizer_description')
            if 'organizer_website' not in columns:
                missing_columns.append('organizer_website')
            if 'advertising_opportunities' not in columns:
                missing_columns.append('advertising_opportunities')
            if 'sponsorship_opportunities' not in columns:
                missing_columns.append('sponsorship_opportunities')
            if 'organizer_profile_updated_at' not in columns:
                missing_columns.append('organizer_profile_updated_at')
            
            # Add missing columns to the User table
            if missing_columns:
                logger.info(f"Adding missing columns to user table: {', '.join(missing_columns)}")
                with db.engine.connect() as conn:
                    if 'is_organizer' in missing_columns:
                        conn.execute('ALTER TABLE "user" ADD COLUMN is_organizer BOOLEAN DEFAULT FALSE')
                    if 'company_name' in missing_columns:
                        conn.execute('ALTER TABLE "user" ADD COLUMN company_name VARCHAR(100)')
                    if 'organizer_description' in missing_columns:
                        conn.execute('ALTER TABLE "user" ADD COLUMN organizer_description TEXT')
                    if 'organizer_website' in missing_columns:
                        conn.execute('ALTER TABLE "user" ADD COLUMN organizer_website VARCHAR(200)')
                    if 'advertising_opportunities' in missing_columns:
                        conn.execute('ALTER TABLE "user" ADD COLUMN advertising_opportunities TEXT')
                    if 'sponsorship_opportunities' in missing_columns:
                        conn.execute('ALTER TABLE "user" ADD COLUMN sponsorship_opportunities TEXT')
                    if 'organizer_profile_updated_at' in missing_columns:
                        conn.execute('ALTER TABLE "user" ADD COLUMN organizer_profile_updated_at TIMESTAMP')
                    
                logger.info("Schema update completed successfully")
            else:
                logger.info("No schema updates needed")
        else:
            logger.warning("User table not found in database")
            
    except Exception as e:
        logger.error(f"Error updating schema: {str(e)}")
        raise

if __name__ == "__main__":
    update_schema()
