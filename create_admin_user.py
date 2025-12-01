import argparse
from werkzeug.security import generate_password_hash
from app import db
from models import User

DEFAULT_EMAIL = "ryan@funlist.ai"
DEFAULT_PASSWORD = "120M2025*v7"
DEFAULT_FIRST_NAME = "Ryan"
DEFAULT_LAST_NAME = "Admin"


def create_admin(email=None, password=None, first_name=None, last_name=None):
    """Create or update an admin user with the provided credentials."""
    email = email or DEFAULT_EMAIL
    password = password or DEFAULT_PASSWORD
    first_name = first_name or DEFAULT_FIRST_NAME
    last_name = last_name or DEFAULT_LAST_NAME

    try:
        # Check if the user already exists
        admin_user = User.query.filter_by(email=email).first()

        if admin_user:
            # Update the existing admin user
            admin_user.password_hash = generate_password_hash(password)
            admin_user.is_admin = True
            admin_user.account_active = True
            admin_user.first_name = admin_user.first_name or first_name
            admin_user.last_name = admin_user.last_name or last_name
            
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
                email=email,
                password_hash=generate_password_hash(password),
                is_admin=True,
                account_active=True,
                first_name=first_name,
                last_name=last_name
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

def parse_args():
    parser = argparse.ArgumentParser(description="Create or update an admin user.")
    parser.add_argument("--email", help=f"Admin email (default: {DEFAULT_EMAIL})")
    parser.add_argument("--password", help="Admin password (default hardcoded fallback)")
    parser.add_argument("--first-name", dest="first_name", help=f"First name (default: {DEFAULT_FIRST_NAME})")
    parser.add_argument("--last-name", dest="last_name", help=f"Last name (default: {DEFAULT_LAST_NAME})")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    from app import create_app
    app = create_app()
    with app.app_context():
        create_admin(
            email=args.email,
            password=args.password,
            first_name=args.first_name,
            last_name=args.last_name,
        )
