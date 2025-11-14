
import logging
from sqlalchemy import inspect, text
from db_init import db
from app import create_app
from models import User, Event, Subscriber

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_schema():
    """Update database schema to match current models"""
    app = create_app()
    with app.app_context():
        try:
            # Check existing columns
            inspector = inspect(db.engine)
            event_columns = [column['name'] for column in inspector.get_columns('events')]
            user_columns = [column['name'] for column in inspector.get_columns('users')]

            # Add missing columns if they don't exist
            with db.engine.connect() as conn:
                if 'parent_event_id' not in event_columns:
                    logger.info("Adding parent_event_id column to events table...")
                    conn.execute(text('ALTER TABLE events ADD COLUMN IF NOT EXISTS parent_event_id INTEGER REFERENCES events(id)'))
                    conn.commit()

                if 'fun_meter' not in event_columns:
                    logger.info("Adding fun_meter column to events table...")
                    conn.execute(text('ALTER TABLE events ADD COLUMN IF NOT EXISTS fun_meter INTEGER DEFAULT 3'))
                    conn.commit()

                if 'is_recurring' not in event_columns:
                    logger.info("Adding is_recurring column to events table...")
                    conn.execute(text('ALTER TABLE events ADD COLUMN IF NOT EXISTS is_recurring BOOLEAN DEFAULT FALSE'))
                    conn.commit()

                if 'recurring_pattern' not in event_columns:
                    logger.info("Adding recurring_pattern column to events table...")
                    conn.execute(text('ALTER TABLE events ADD COLUMN IF NOT EXISTS recurring_pattern VARCHAR(50)'))
                    conn.commit()

                if 'recurring_end_date' not in event_columns:
                    logger.info("Adding recurring_end_date column to events table...")
                    conn.execute(text('ALTER TABLE events ADD COLUMN IF NOT EXISTS recurring_end_date TIMESTAMP'))
                    conn.commit()

                social_columns = {
                    'facebook_url': 'VARCHAR(255)',
                    'instagram_url': 'VARCHAR(255)',
                    'twitter_url': 'VARCHAR(255)',
                    'linkedin_url': 'VARCHAR(255)',
                    'tiktok_url': 'VARCHAR(255)',
                }

                for column_name, column_type in social_columns.items():
                    if column_name not in user_columns:
                        logger.info(f"Adding {column_name} column to users table...")
                        conn.execute(text(f'ALTER TABLE users ADD COLUMN IF NOT EXISTS {column_name} {column_type}'))
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
