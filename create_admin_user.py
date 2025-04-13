import os
import sys
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import db
from models import User

def create_admin():
    """Create an admin user with the specified credentials."""
    try:
        # Check if the user already exists
        admin_user = User.query.filter_by(email="ryan@funlist.ai").first()
        
        if admin_user:
            # Update the existing admin user
            admin_user.password_hash = generate_password_hash("120M2025*v7")
            admin_user.is_admin = True
            admin_user.account_active = True
            
            # Ensure all the fields added in the role update are populated
            if hasattr(admin_user, 'is_subscriber'):
                admin_user.is_subscriber = True
            if hasattr(admin_user, 'is_event_creator_last_known'):
                admin_user.is_event_creator_last_known = admin_user.is_event_creator
            if hasattr(admin_user, 'is_organizer_last_known'):
                admin_user.is_organizer_last_known = admin_user.is_organizer
            if hasattr(admin_user, 'is_vendor_last_known'):
                admin_user.is_vendor_last_known = admin_user.is_vendor
            if hasattr(admin_user, 'is_sponsor_last_known'):
                admin_user.is_sponsor_last_known = admin_user.is_sponsor
            
            print(f"Updated existing admin user: {admin_user.email}")
        else:
            # Create a new admin user
            new_admin = User(
                email="ryan@funlist.ai",
                password_hash=generate_password_hash("120M2025*v7"),
                is_admin=True,
                account_active=True,
                first_name="Ryan",
                last_name="Admin"
            )
            
            # Set role fields if they exist
            if hasattr(new_admin, 'is_subscriber'):
                new_admin.is_subscriber = True
            if hasattr(new_admin, 'is_event_creator_last_known'):
                new_admin.is_event_creator_last_known = False
            if hasattr(new_admin, 'is_organizer_last_known'):
                new_admin.is_organizer_last_known = False
            if hasattr(new_admin, 'is_vendor_last_known'):
                new_admin.is_vendor_last_known = False
            if hasattr(new_admin, 'is_sponsor_last_known'):
                new_admin.is_sponsor_last_known = False
            
            db.session.add(new_admin)
            print(f"Created new admin user: {new_admin.email}")
        
        db.session.commit()
        print("Admin user saved successfully!")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error creating/updating admin user: {str(e)}")
        return False

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        create_admin()