import logging
from sqlalchemy import inspect, text
from db_init import db
from app import create_app
from models import User, Event, Subscriber

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def update_schema():
    """Update database schema to match current models"""
    app = create_app()

    with app.app_context():
        inspector = inspect(db.engine)

        # Check Event table
        if 'events' in inspector.get_table_names():
            event_columns = [column['name'] for column in inspector.get_columns('events')]

            # Add missing columns
            missing_columns = []
            required_columns = [
                ('location', 'VARCHAR(255)'),
                ('street', 'VARCHAR(255)'),
                ('target_audience', 'VARCHAR(255)'),
                ('fun_meter', 'INTEGER DEFAULT 3'),
                ('status', 'VARCHAR(50) DEFAULT \'pending\'')
            ]

            for col_name, col_type in required_columns:
                if col_name not in event_columns:
                    missing_columns.append((col_name, col_type))

            if missing_columns:
                logger.info(f"Adding missing columns to events table: {[col[0] for col in missing_columns]}")

                for col_name, col_type in missing_columns:
                    try:
                        db.session.execute(text(f"ALTER TABLE events ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                    except Exception as e:
                        logger.error(f"Error adding column {col_name}: {str(e)}")

                db.session.commit()
                logger.info("Events schema update completed")

        else:
            logger.info("Events table not found, will be created by db.create_all()")
            db.create_all()


        # Check existing columns in user table
        try:
            columns = [c['name'] for c in inspector.get_columns('user')]

            # Add new columns if they don't exist
            with db.engine.connect() as conn:
                if 'is_subscriber' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN is_subscriber BOOLEAN DEFAULT TRUE'))
                    conn.commit()
                    logger.info("Added is_subscriber column")

                if 'is_event_creator' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN is_event_creator BOOLEAN DEFAULT FALSE'))
                    conn.commit()
                    logger.info("Added is_event_creator column")

                if 'is_organizer' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN is_organizer BOOLEAN DEFAULT FALSE'))
                    conn.commit()
                    logger.info("Added is_organizer column")

                if 'company_name' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN company_name VARCHAR(100)'))
                    conn.commit()
                    logger.info("Added company_name column")

                if 'organizer_description' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN organizer_description TEXT'))
                    conn.commit()
                    logger.info("Added organizer_description column")

                if 'organizer_website' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN organizer_website VARCHAR(200)'))
                    conn.commit()
                    logger.info("Added organizer_website column")

                if 'advertising_opportunities' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN advertising_opportunities TEXT'))
                    conn.commit()
                    logger.info("Added advertising_opportunities column")

                if 'sponsorship_opportunities' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN sponsorship_opportunities TEXT'))
                    conn.commit()
                    logger.info("Added sponsorship_opportunities column")

                if 'organizer_profile_updated_at' not in columns:
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN organizer_profile_updated_at TIMESTAMP'))
                    conn.commit()
                    logger.info("Added organizer_profile_updated_at column")

                # Update existing users
                conn.execute(text('UPDATE "user" SET is_subscriber = TRUE WHERE is_subscriber IS NULL'))
                conn.commit()

                # Update admin user
                conn.execute(text('UPDATE "user" SET is_subscriber = TRUE, is_event_creator = TRUE, is_admin = TRUE WHERE email = \'ryan@americanmarketingalliance.com\''))
                conn.commit()

                if 'is_organizer' in columns:
                    conn.execute(text('UPDATE "user" SET is_organizer = TRUE WHERE email = \'ryan@americanmarketingalliance.com\''))
                    conn.commit()

            logger.info("User schema update completed successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating user schema: {str(e)}")
            return False

if __name__ == "__main__":
    success = update_schema()
    if success:
        print("Schema updated successfully.")
    else:
        print("Failed to update schema.")