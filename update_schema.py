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
            columns = [column['name'] for column in inspector.get_columns('events')]

            # Add missing columns if they don't exist
            with db.engine.connect() as conn:
                if 'parent_event_id' not in columns:
                    logger.info("Adding parent_event_id column to events table...")
                    conn.execute(text('ALTER TABLE events ADD COLUMN IF NOT EXISTS parent_event_id INTEGER REFERENCES events(id)'))
                    conn.commit()
                    logger.info("Added parent_event_id column")

                if 'fun_meter' not in columns:
                    logger.info("Adding fun_meter column to events table...")
                    conn.execute(text('ALTER TABLE events ADD COLUMN IF NOT EXISTS fun_meter INTEGER DEFAULT 3'))
                    conn.commit()
                    logger.info("Added fun_meter column")

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