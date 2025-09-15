
from flask_migrate import Migrate
from app import create_app
from db_init import db
from models import Event
from sqlalchemy import Column, Text, inspect
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_event_model():
    """Update the Event model with new fields for fun rating justification and target audience description"""
    app = create_app()

    with app.app_context():
        try:
            # Check if the columns already exist using database-agnostic approach
            inspector = inspect(db.engine)
            columns = [column['name'] for column in inspector.get_columns('event')]
            
            logger.info(f"Existing columns in event table: {columns}")
            
            # Add the new columns if they don't exist
            with db.engine.connect() as conn:
                # Use transactions for better reliability
                conn = conn.execution_options(isolation_level="AUTOCOMMIT")
                
                # Determine database type to use appropriate SQL syntax
                dialect = db.engine.dialect.name
                logger.info(f"Database dialect: {dialect}")
                
                if 'fun_rating_justification' not in columns:
                    logger.info("Adding fun_rating_justification field to Event model...")
                    try:
                        if dialect == 'postgresql':
                            conn.execute(db.text('ALTER TABLE event ADD COLUMN IF NOT EXISTS fun_rating_justification TEXT'))
                        else: # SQLite and others
                            conn.execute(db.text('ALTER TABLE event ADD COLUMN fun_rating_justification TEXT'))
                        logger.info("Field fun_rating_justification added successfully")
                    except Exception as e:
                        logger.error(f"Error adding fun_rating_justification column: {e}")
                else:
                    logger.info("Field fun_rating_justification already exists")
                
                if 'target_audience_description' not in columns:
                    logger.info("Adding target_audience_description field to Event model...")
                    try:
                        if dialect == 'postgresql':
                            conn.execute(db.text('ALTER TABLE event ADD COLUMN IF NOT EXISTS target_audience_description TEXT'))
                        else: # SQLite and others
                            conn.execute(db.text('ALTER TABLE event ADD COLUMN target_audience_description TEXT'))
                        logger.info("Field target_audience_description added successfully")
                    except Exception as e:
                        logger.error(f"Error adding target_audience_description column: {e}")
                else:
                    logger.info("Field target_audience_description already exists")
            
            # Ensure SQLAlchemy knows about these new columns
            db.session.commit()
            db.metadata.clear()
            db.reflect()
            logger.info("Database updated successfully")
        except Exception as e:
            logger.error(f"Error updating database: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    update_event_model()
