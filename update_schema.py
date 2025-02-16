from app import app
from models import User, Event, Subscriber
from db_init import db
import logging

logger = logging.getLogger(__name__)

def update_schema():
    with app.app_context():
        # Create all tables
        db.create_all()
        logger.info("Database schema updated successfully.")

if __name__ == "__main__":
    update_schema()