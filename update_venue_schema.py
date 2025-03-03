
from db_init import db
from app import create_app
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def update_venue_schema():
    app = create_app()
    with app.app_context():
        try:
            # Check existing columns
            inspector = db.inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('user')]
            
            # Add venue columns if they don't exist
            with db.engine.connect() as conn:
                if 'is_venue' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN is_venue BOOLEAN DEFAULT FALSE'))
                    conn.commit()
                    logger.info("Added is_venue column")
                
                if 'venue_capacity' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN venue_capacity VARCHAR(50)'))
                    conn.commit()
                    logger.info("Added venue_capacity column")
                
                if 'venue_features' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN venue_features TEXT'))
                    conn.commit()
                    logger.info("Added venue_features column")
                
                if 'venue_profile_updated_at' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN venue_profile_updated_at TIMESTAMP'))
                    conn.commit()
                    logger.info("Added venue_profile_updated_at column")
                
                # Add vendor columns if they don't exist
                if 'services' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN services TEXT'))
                    conn.commit()
                    logger.info("Added services column")
                
                if 'pricing' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN pricing TEXT'))
                    conn.commit()
                    logger.info("Added pricing column")
                
                # Add venue_id to events table
                event_columns = [c['name'] for c in inspector.get_columns('event')]
                if 'venue_id' not in event_columns:
                    conn.execute(text('ALTER TABLE "event" ADD COLUMN venue_id INTEGER REFERENCES "user" (id)'))
                    conn.commit()
                    logger.info("Added venue_id column to events table")
                
            logger.info("Venue and vendor schema update complete!")
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")
            return False
        return True

if __name__ == "__main__":
    update_venue_schema()
