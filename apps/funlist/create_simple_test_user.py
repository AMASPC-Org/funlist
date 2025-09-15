from app import create_app
from models import db, User
import os
from datetime import datetime

def create_test_user():
    """Create a test user with all roles enabled for testing"""
    app = create_app()
    with app.app_context():
        # Check if the test user already exists
        test_user = User.query.filter_by(email="test@funlist.ai").first()
        if test_user:
            print(f"Test user already exists with ID: {test_user.id}")
            return test_user

        # Create a new test user with all roles enabled
        new_user = User(
            email="test@funlist.ai",
            first_name="Test",
            last_name="User",
            account_active=True,
            is_admin=False,
            is_subscriber=True,
            _is_event_creator=True,
            is_organizer=True,
            is_vendor=True,
            is_sponsor=True,
            roles_last_updated=datetime.utcnow()
        )
        
        # Set password using the proper method
        new_user.set_password("password123")
        
        db.session.add(new_user)
        try:
            db.session.commit()
            print(f"Test user created successfully with ID: {new_user.id}")
            return new_user
        except Exception as e:
            db.session.rollback()
            print(f"Error creating test user: {str(e)}")
            return None

if __name__ == "__main__":
    create_test_user()