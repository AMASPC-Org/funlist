
from flask import Flask
from models import User, Event, Subscriber
from db_init import db
import logging
from sqlalchemy import inspect

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///funlist.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def update_schema():
    app = create_app()
    with app.app_context():
        try:
            # Get existing tables and columns
            inspector = inspect(db.engine)
            
            # Check if User table has is_organizer column
            user_columns = [col['name'] for col in inspector.get_columns('user')]
            
            # Add organizer columns if they don't exist
            if 'is_organizer' not in user_columns:
                logger.info("Adding organizer columns to User table")
                
                # Use SQL to add the missing columns
                db.session.execute(db.text('ALTER TABLE "user" ADD COLUMN is_organizer BOOLEAN DEFAULT FALSE'))
                db.session.execute(db.text('ALTER TABLE "user" ADD COLUMN company_name VARCHAR(100)'))
                db.session.execute(db.text('ALTER TABLE "user" ADD COLUMN organizer_description TEXT'))
                db.session.execute(db.text('ALTER TABLE "user" ADD COLUMN organizer_website VARCHAR(200)'))
                db.session.execute(db.text('ALTER TABLE "user" ADD COLUMN advertising_opportunities TEXT'))
                db.session.execute(db.text('ALTER TABLE "user" ADD COLUMN sponsorship_opportunities TEXT'))
                db.session.execute(db.text('ALTER TABLE "user" ADD COLUMN organizer_profile_updated_at TIMESTAMP'))
                
                db.session.commit()
                logger.info("Added organizer columns to User table")
            else:
                logger.info("Organizer columns already exist in User table")
                
        except Exception as e:
            logger.error(f"Error updating schema: {str(e)}")
            logger.info("Recreating all tables from scratch")
            db.drop_all()
            db.create_all()
            logger.info("Database schema recreated from scratch")

if __name__ == "__main__":
    update_schema()
