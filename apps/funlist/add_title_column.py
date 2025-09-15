
from app import create_app
from db_init import db
from sqlalchemy import text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def add_title_column():
    app = create_app()
    with app.app_context():
        try:
            # Check if title column exists
            inspector = db.inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('users')]
            
            if 'title' not in columns:
                logger.info("Adding 'title' column to users table")
                db.session.execute(text("ALTER TABLE users ADD COLUMN title VARCHAR(100)"))
                db.session.commit()
                logger.info("Successfully added 'title' column to users table")
                
                # If organizer_title exists, migrate data from there to title
                if 'organizer_title' in columns:
                    logger.info("Migrating data from organizer_title to title")
                    db.session.execute(text("UPDATE users SET title = organizer_title WHERE organizer_title IS NOT NULL"))
                    db.session.commit()
                    logger.info("Data migration completed successfully")
            else:
                logger.info("'title' column already exists in users table")
                
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error adding title column: {str(e)}")
            return False

if __name__ == "__main__":
    success = add_title_column()
    if success:
        print("Title column added successfully to users table.")
    else:
        print("Failed to add title column to users table.")
