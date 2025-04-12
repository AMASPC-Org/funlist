
import os
import sys
import logging
from app import create_app
from db_init import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import inspect
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

def migrate_schema():
    try:
        app = create_app()
        with app.app_context():
            # Get SQLAlchemy inspector
            inspector = inspect(db.engine)
            
            # Check if venue_types table exists
            if "venue_types" not in inspector.get_table_names():
                logger.info("Creating venue_types table")
                db.engine.execute('''
                CREATE TABLE venue_types (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    category VARCHAR(100)
                )
                ''')
                logger.info("venue_types table created successfully")
            
            # Check if venues table exists
            if "venues" not in inspector.get_table_names():
                logger.info("Creating venues table")
                db.engine.execute('''
                CREATE TABLE venues (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    street VARCHAR(255) NOT NULL,
                    city VARCHAR(100) NOT NULL,
                    state VARCHAR(100) NOT NULL,
                    zip_code VARCHAR(20) NOT NULL,
                    country VARCHAR(100) DEFAULT 'United States',
                    phone VARCHAR(20),
                    email VARCHAR(120),
                    website VARCHAR(255),
                    venue_type_id INTEGER,
                    contact_name VARCHAR(200),
                    contact_phone VARCHAR(20),
                    contact_email VARCHAR(120),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER,
                    FOREIGN KEY (venue_type_id) REFERENCES venue_types (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
                ''')
                logger.info("venues table created successfully")
            
            # Check if we need to add venue_id to events table
            events_columns = [c['name'] for c in inspector.get_columns('events')]
            if "venue_id" not in events_columns:
                logger.info("Adding venue_id column to events table")
                db.engine.execute('ALTER TABLE events ADD COLUMN venue_id INTEGER REFERENCES venues(id)')
                logger.info("venue_id column added successfully")
            
            # Check for title field in users table
            users_columns = [c['name'] for c in inspector.get_columns('users')]
            
            # Add title field if it doesn't exist
            if "title" not in users_columns:
                logger.info("Adding title column to users table")
                db.engine.execute('ALTER TABLE users ADD COLUMN title VARCHAR(100)')
                logger.info("title column added successfully")
                
                # Transfer data from organizer_title to title if applicable
                if "organizer_title" in users_columns:
                    logger.info("Transferring data from organizer_title to title")
                    db.engine.execute('UPDATE users SET title = organizer_title WHERE organizer_title IS NOT NULL')
                    logger.info("Data transfer completed successfully")
            
            # Remove location from users table if it exists (optional)
            # This is commented out to prevent data loss, as you might want to keep this data
            # if "location" in users_columns:
            #     logger.info("Removing location column from users table")
            #     db.engine.execute('ALTER TABLE users DROP COLUMN location')
            #     logger.info("location column removed successfully")
            
            logger.info("Schema migration completed successfully")
            
    except Exception as e:
        logger.error(f"Error migrating schema: {str(e)}")

if __name__ == "__main__":
    migrate_schema()
    print("Done!")
