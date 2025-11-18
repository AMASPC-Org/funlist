
#!/usr/bin/env python3
"""
Migration script to add OAuth columns to users table
Run this once to update the database schema for OAuth support
"""
import os
import sys
from sqlalchemy import create_engine, text, Column, String, Boolean
from sqlalchemy.exc import OperationalError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_schema():
    """Add OAuth columns to users table"""
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        logger.error("DATABASE_URL environment variable not set")
        return False
    
    engine = create_engine(database_url)
    
    columns_to_add = [
        ("oauth_provider", "VARCHAR(20)"),
        ("oauth_provider_id", "VARCHAR(255) UNIQUE"),
        ("email_verified", "BOOLEAN DEFAULT FALSE")
    ]
    
    try:
        with engine.connect() as conn:
            for column_name, column_type in columns_to_add:
                try:
                    # Check if column exists
                    result = conn.execute(text(
                        f"SELECT column_name FROM information_schema.columns "
                        f"WHERE table_name='users' AND column_name='{column_name}'"
                    ))
                    
                    if result.fetchone() is None:
                        # Add column
                        conn.execute(text(
                            f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"
                        ))
                        conn.commit()
                        logger.info(f"✅ Added column: {column_name}")
                    else:
                        logger.info(f"ℹ️  Column already exists: {column_name}")
                        
                except OperationalError as e:
                    logger.warning(f"⚠️  Could not add {column_name}: {str(e)}")
                    continue
        
        logger.info("✅ OAuth schema migration completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = update_schema()
    sys.exit(0 if success else 1)
