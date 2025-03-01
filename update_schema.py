
from app import app
from models import User, Event, Subscriber
from db_init import db
import logging
import sqlalchemy as sa
from sqlalchemy import inspect

logger = logging.getLogger(__name__)

def update_schema():
    with app.app_context():
        # Get existing tables and columns
        inspector = inspect(db.engine)
        
        # Check if User table has is_organizer column
        user_columns = [col['name'] for col in inspector.get_columns('user')]
        
        # Add organizer columns if they don't exist
        if 'is_organizer' not in user_columns:
            try:
                # Add organizer fields to User table
                db.engine.execute('ALTER TABLE "user" ADD COLUMN is_organizer BOOLEAN DEFAULT FALSE')
                db.engine.execute('ALTER TABLE "user" ADD COLUMN company_name VARCHAR(100)')
                db.engine.execute('ALTER TABLE "user" ADD COLUMN organizer_description TEXT')
                db.engine.execute('ALTER TABLE "user" ADD COLUMN organizer_website VARCHAR(200)')
                db.engine.execute('ALTER TABLE "user" ADD COLUMN advertising_opportunities TEXT')
                db.engine.execute('ALTER TABLE "user" ADD COLUMN sponsorship_opportunities TEXT')
                db.engine.execute('ALTER TABLE "user" ADD COLUMN organizer_profile_updated_at TIMESTAMP')
                
                logger.info("Added organizer columns to User table")
            except Exception as e:
                logger.error(f"Error adding organizer columns: {e}")
                # If above method fails, recreate tables
                db.drop_all()
                db.create_all()
                logger.info("Database schema recreated from scratch")
        else:
            logger.info("Organizer columns already exist in User table")

if __name__ == "__main__":
    update_schema()
