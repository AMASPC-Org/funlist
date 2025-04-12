from app import create_app
from db_init import db
from sqlalchemy import text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def migrate_venue_schema():
    app = create_app()
    with app.app_context():
        try:
            # Check existing tables and columns
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()

            # Create venue_types table if it doesn't exist
            if 'venue_types' not in tables:
                logger.info("Creating venue_types table")
                db.session.execute(text('''
                CREATE TABLE venue_types (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    category VARCHAR(100),
                    description TEXT
                )
                '''))
                db.session.commit()
                logger.info("venue_types table created successfully")

            # Create venues table if it doesn't exist
            if 'venues' not in tables:
                logger.info("Creating venues table")
                db.session.execute(text('''
                CREATE TABLE venues (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    street VARCHAR(100),
                    city VARCHAR(50),
                    state VARCHAR(50),
                    zip_code VARCHAR(20),
                    country VARCHAR(50) DEFAULT 'United States',
                    phone VARCHAR(20),
                    email VARCHAR(120),
                    website VARCHAR(200),
                    venue_type_id INTEGER REFERENCES venue_types(id),
                    contact_name VARCHAR(100),
                    contact_phone VARCHAR(20),
                    contact_email VARCHAR(120),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER REFERENCES users(id)
                )
                '''))
                db.session.commit()
                logger.info("venues table created successfully")

            # Check if venue_id column exists in events table
            events_columns = [c['name'] for c in inspector.get_columns('events')]
            if "venue_id" not in events_columns:
                logger.info("Adding venue_id column to events table")
                db.session.execute(text('ALTER TABLE events ADD COLUMN venue_id INTEGER REFERENCES venues(id)'))
                db.session.commit()
                logger.info("venue_id column added successfully")

            # Check for title field in users table and add if it doesn't exist
            users_columns = [c['name'] for c in inspector.get_columns('users')]
            if "title" not in users_columns:
                logger.info("Adding title column to users table")
                db.session.execute(text('ALTER TABLE users ADD COLUMN title VARCHAR(100)'))
                db.session.commit()
                logger.info("title column added successfully")

                # Transfer data from organizer_title to title if applicable
                if "organizer_title" in users_columns:
                    logger.info("Transferring data from organizer_title to title")
                    db.session.execute(text('UPDATE users SET title = organizer_title WHERE organizer_title IS NOT NULL'))
                    db.session.commit()
                    logger.info("Data transfer completed successfully")

            logger.info("Schema migration completed successfully")
            return True

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error migrating schema: {str(e)}")
            return False

if __name__ == "__main__":
    success = migrate_venue_schema()
    if success:
        print("Venue schema migration completed successfully.")
    else:
        print("Failed to migrate venue schema.")