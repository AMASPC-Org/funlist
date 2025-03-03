
#!/usr/bin/env python3

from app import create_app
from models import User
from db_init import db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_vendor_schema():
    app = create_app()
    with app.app_context():
        try:
            # Check existing columns
            inspector = db.inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('user')]
            
            # Add new columns if they don't exist
            with db.engine.connect() as conn:
                if 'is_vendor' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN is_vendor BOOLEAN DEFAULT FALSE'))
                    conn.commit()
                    logger.info("Added is_vendor column")
                
                if 'vendor_type' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN vendor_type VARCHAR(50)'))
                    conn.commit()
                    logger.info("Added vendor_type column")
                
                if 'vendor_description' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN vendor_description TEXT'))
                    conn.commit()
                    logger.info("Added vendor_description column")
                
                if 'vendor_profile_updated_at' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN vendor_profile_updated_at TIMESTAMP'))
                    conn.commit()
                    logger.info("Added vendor_profile_updated_at column")
                
            logger.info("Schema update complete!")
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")
            logger.error("Schema update failed.")

if __name__ == "__main__":
    update_vendor_schema()
