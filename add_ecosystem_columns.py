import os
from sqlalchemy import text
from app_config import prepare_database_config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_ecosystem_columns():
    try:
        # Load db config natively
        db_config = prepare_database_config(logger)
        
        # We need SQLAlchemy engine to execute raw SQL reliably
        from sqlalchemy import create_engine
        engine = create_engine(db_config.database_url, **db_config.engine_options)

        with engine.connect() as conn:
            with conn.begin():
                logger.info("Adding origin_site column...")
                conn.execute(text("ALTER TABLE events ADD COLUMN IF NOT EXISTS origin_site VARCHAR(50) DEFAULT 'funlist';"))
                
                logger.info("Adding visibility_tags column...")
                conn.execute(text("ALTER TABLE events ADD COLUMN IF NOT EXISTS visibility_tags JSON;"))
                
                logger.info("Adding confidence_score column...")
                conn.execute(text("ALTER TABLE events ADD COLUMN IF NOT EXISTS confidence_score DECIMAL(3,2) DEFAULT 0.00;"))
                
                logger.info("Adding is_ai_enriched column...")
                conn.execute(text("ALTER TABLE events ADD COLUMN IF NOT EXISTS is_ai_enriched BOOLEAN DEFAULT FALSE;"))
                
                logger.info("Adding enrichment_data column...")
                conn.execute(text("ALTER TABLE events ADD COLUMN IF NOT EXISTS enrichment_data JSONB;"))

        logger.info("Successfully added all cross-site ecosystem columns to the events table.")
        
    except Exception as e:
        logger.error(f"Failed to add ecosystem columns: {e}")
        raise

if __name__ == "__main__":
    add_ecosystem_columns()
