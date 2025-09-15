
from db_init import db
from models import User
from app import create_app
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_user():
    """Create a test user for login testing"""
    app = create_app()
    
    # Ensure the instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    with app.app_context():
        try:
            # Check if user already exists
            user = User.query.filter_by(email="user@example.com").first()
            
            if user:
                logger.info("Test user already exists. Updating password...")
                user.set_password("user123")
            else:
                logger.info("Creating new test user...")
                user = User(
                    email="user@example.com",
                    account_active=True,
                    is_event_creator=True
                )
                user.set_password("user123")
                db.session.add(user)
            
            # Also create admin user if needed
            admin = User.query.filter_by(email="admin@example.com").first()
            
            if not admin:
                logger.info("Creating admin user...")
                admin = User(
                    email="admin@example.com",
                    account_active=True,
                    is_admin=True,
                    is_event_creator=True,
                    is_organizer=True
                )
                admin.set_password("admin123")
                db.session.add(admin)
            
            db.session.commit()
            logger.info("Test users created successfully!")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating test users: {str(e)}")
            print(f"Error: {str(e)}")
            return False

if __name__ == "__main__":
    success = create_test_user()
    if success:
        print("Test users created successfully.")
        print("You can log in with:")
        print("Email: user@example.com")
        print("Password: user123")
        print("Or admin:")
        print("Email: admin@example.com")
        print("Password: admin123")
    else:
        print("Failed to create test users.")
