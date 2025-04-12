
from db_init import db
from app import create_app
import logging
from sqlalchemy import text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_featured_column():
    try:
        logger.info("Starting fix for featured column...")
        app = create_app()
        with app.app_context():
            # Check if the column exists
            try:
                db.session.execute(text("SELECT is_featured FROM events LIMIT 1"))
                logger.info("Found 'is_featured' column, renaming to 'featured'")
                db.session.execute(text("ALTER TABLE events RENAME COLUMN is_featured TO featured"))
                db.session.commit()
                logger.info("Column renamed successfully")
            except Exception as e:
                logger.info(f"Column 'is_featured' doesn't exist: {str(e)}")
                try:
                    # Try to check if featured column exists
                    db.session.execute(text("SELECT featured FROM events LIMIT 1"))
                    logger.info("Found 'featured' column, no changes needed")
                except Exception as e2:
                    logger.info(f"Column 'featured' doesn't exist either: {str(e2)}")
                    # Create the column if it doesn't exist
                    logger.info("Creating 'featured' column")
                    db.session.execute(text("ALTER TABLE events ADD COLUMN featured BOOLEAN DEFAULT FALSE"))
                    db.session.commit()
                    logger.info("Column created successfully")
        
        logger.info("Fix completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error fixing featured column: {str(e)}")
        return False

if __name__ == "__main__":
    fix_featured_column()
