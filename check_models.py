
from app import create_app
from models import User, Event, Subscriber
from db_init import db
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_models():
    app = create_app()
    with app.app_context():
        try:
            # Check User model
            logger.info("Checking User model...")
            user_columns = [column.name for column in User.__table__.columns]
            logger.info(f"User columns: {', '.join(user_columns)}")
            
            # Check Event model
            logger.info("Checking Event model...")
            event_columns = [column.name for column in Event.__table__.columns]
            logger.info(f"Event columns: {', '.join(event_columns)}")
            
            # Check relationships
            logger.info("Checking relationships...")
            user = User.query.first()
            if user:
                logger.info(f"Found user: {user.email}")
                events = Event.query.filter_by(user_id=user.id).all()
                logger.info(f"User has {len(events)} events")
            
            logger.info("Model check completed successfully")
        except Exception as e:
            logger.error(f"Error checking models: {str(e)}", exc_info=True)
            sys.exit(1)

if __name__ == "__main__":
    check_models()
