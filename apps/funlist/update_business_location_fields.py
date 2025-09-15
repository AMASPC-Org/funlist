
from app import create_app
from db_init import db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_business_location_schema():
    app = create_app()
    with app.app_context():
        try:
            # Check existing columns
            inspector = db.inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('users')]
            
            # Add new columns if they don't exist
            with db.engine.connect() as conn:
                if 'business_street' not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN business_street VARCHAR(100)'))
                    logger.info("Added business_street column")
                
                if 'business_city' not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN business_city VARCHAR(50)'))
                    logger.info("Added business_city column")
                
                if 'business_state' not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN business_state VARCHAR(50)'))
                    logger.info("Added business_state column")
                
                if 'business_zip' not in columns:
                    conn.execute(text('ALTER TABLE users ADD COLUMN business_zip VARCHAR(20)'))
                    logger.info("Added business_zip column")
                
                # Commit the transaction
                conn.commit()
                
            logger.info("Schema update complete!")
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")

if __name__ == "__main__":
    update_business_location_schema()
