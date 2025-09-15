#!/usr/bin/env python3

from models import User
from db_init import db
from app import create_app
from werkzeug.security import generate_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_or_update_user(email, password, is_subscriber=True, is_event_creator=False, is_organizer=False, is_admin=False):
    """Create or update a user with specific permissions"""
    app = create_app()
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
    # Update ryan.r.rutledge@gmail.com permissions
    user_success = create_or_update_user(
        'ryan.r.rutledge@gmail.com',
        '120M2025*v7',
        is_subscriber=True,
        is_event_creator=True,
        is_organizer=False,
        is_admin=False
    )
    logger.info(f"User setup: {'Success' if user_success else 'Failed'}")