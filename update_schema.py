from app import create_app
from db_init import db
import logging
from sqlalchemy import text

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d',
    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

def update_schema():
    app = create_app()
    with app.app_context():
        try:
            # Check existing columns
            inspector = db.inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('user')]

            # Add user profile columns if they don't exist
            with db.engine.connect() as conn:
                if 'audience_type' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN audience_type VARCHAR(200)'))
                    conn.commit()
                    logger.info("Added audience_type column")

                if 'preferred_locations' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN preferred_locations VARCHAR(255)'))
                    conn.commit()
                    logger.info("Added preferred_locations column")

                if 'event_interests' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN event_interests VARCHAR(255) NULL'))
                    conn.commit()
                    logger.info("Added event_interests column")

                # Add is_premium field if it doesn't exist
                if 'is_premium' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN is_premium BOOLEAN DEFAULT FALSE'))
                    conn.commit()
                    logger.info("Added is_premium column")

                # Add venue columns if they don't exist
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

            logger.info("Schema update complete!")
            return True
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")
            return False

if __name__ == "__main__":
    update_schema()