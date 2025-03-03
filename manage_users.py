
#!/usr/bin/env python3

from models import User
from db_init import db
from app import app
from werkzeug.security import generate_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_or_update_user(email, password, is_subscriber=True, is_event_creator=False, is_organizer=False, is_admin=False):
    """Create or update a user with specific permissions"""
    with app.app_context():
        try:
            # Check if user exists
            user = User.query.filter_by(email=email).first()
            
            if user:
                logger.info(f"Updating existing user: {email}")
                # Update existing user
                user.password_hash = generate_password_hash(password)
                user.is_subscriber = is_subscriber
                user.is_event_creator = is_event_creator
                user.is_organizer = is_organizer
                user.is_admin = is_admin
                user.account_active = True
            else:
                logger.info(f"Creating new user: {email}")
                # Create new user
                user = User(
                    email=email,
                    password_hash=generate_password_hash(password),
                    is_subscriber=is_subscriber,
                    is_event_creator=is_event_creator,
                    is_organizer=is_organizer,
                    is_admin=is_admin,
                    account_active=True
                )
                db.session.add(user)
            
            db.session.commit()
            
            # Verify changes
            user = User.query.filter_by(email=email).first()
            logger.info(f"User roles for {email}:")
            logger.info(f"  Subscriber: {user.is_subscriber}")
            logger.info(f"  Event Creator: {user.is_event_creator}")
            logger.info(f"  Organizer: {user.is_organizer}")
            logger.info(f"  Admin: {user.is_admin}")
            
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating/updating user {email}: {str(e)}")
            return False

if __name__ == "__main__":
    # Admin user - Only ryan@funlist.ai should be admin
    admin_success = create_or_update_user(
        'ryan@funlist.ai',
        '120M2025*v7',
        is_subscriber=True,
        is_event_creator=True,
        is_organizer=True,
        is_admin=True
    )
    logger.info(f"Admin user setup: {'Success' if admin_success else 'Failed'}")
    
    # Ryan Rutledge - Find events to attend (not admin)
    subscriber_success = create_or_update_user(
        'ryan.r.rutledge@gmail.com',
        '120M2025*v7',
        is_subscriber=True,
        is_event_creator=False,
        is_organizer=False,
        is_admin=False
    )
    logger.info(f"Subscriber user setup: {'Success' if subscriber_success else 'Failed'}")
    
    # Thurston Marketing Alliance - Create and list events
    event_creator_success = create_or_update_user(
        'ryan@thurstonmarketingalliance.com',
        '120M2025*v7',
        is_subscriber=True,
        is_event_creator=True,
        is_organizer=False,
        is_admin=False
    )
    logger.info(f"Event creator user setup: {'Success' if event_creator_success else 'Failed'}")
    
    # Venue - Organization/venue representative
    organizer_success = create_or_update_user(
        'venue@funlist.ai',
        '120M2025*v7',
        is_subscriber=True,
        is_event_creator=True,
        is_organizer=True,
        is_admin=False
    )
    logger.info(f"Organizer user setup: {'Success' if organizer_success else 'Failed'}")
    
    logger.info("User management complete.")
