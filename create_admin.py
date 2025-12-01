
import os
import argparse
from flask import Flask
from models import User
from db_init import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "ryan@americanmarketingalliance.com")
DEFAULT_ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "120M2025*v7")
DEFAULT_FIRST_NAME = os.environ.get("ADMIN_FIRST_NAME", "Admin")
DEFAULT_LAST_NAME = os.environ.get("ADMIN_LAST_NAME", "User")


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def create_admin_user(email=None, password=None, first_name=None, last_name=None):
    app = create_app()
    with app.app_context():
        try:
            # Check if admin user already exists
            admin_email = email or DEFAULT_ADMIN_EMAIL
            admin_password = password or DEFAULT_ADMIN_PASSWORD
            admin_first = first_name or DEFAULT_FIRST_NAME
            admin_last = last_name or DEFAULT_LAST_NAME
            
            # First make sure the schema is updated
            from update_schema import update_schema
            update_schema()
            
            # Now create or update the admin
            admin = User.query.filter_by(email=admin_email).first()
            if admin:
                logger.info(f"Admin user already exists: {admin_email}")
                admin.is_admin = True
                admin.is_subscriber = True
                admin.is_event_creator = True
                admin.is_organizer = True
                admin.account_active = True
                admin.set_password(admin_password)
                if admin_first:
                    admin.first_name = admin_first
                if admin_last:
                    admin.last_name = admin_last
                db.session.commit()
                logger.info(f"Admin user updated with new credentials and all roles")
            else:
                # Create new admin user
                admin = User(
                    email=admin_email,
                    is_admin=True,
                    is_subscriber=True,
                    is_event_creator=True,
                    is_organizer=True,
                    account_active=True,
                    first_name=admin_first,
                    last_name=admin_last
                )
                admin.set_password(admin_password)
                db.session.add(admin)
                db.session.commit()
                logger.info(f"Admin user created: {admin_email}")
            
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating admin user: {str(e)}")
            return False


def parse_args():
    parser = argparse.ArgumentParser(description="Create or update an admin user.")
    parser.add_argument("--email", help=f"Admin email (default: {DEFAULT_ADMIN_EMAIL})")
    parser.add_argument("--password", help="Admin password (default: value from env ADMIN_PASSWORD or built-in default)")
    parser.add_argument("--first-name", dest="first_name", help=f"First name (default: {DEFAULT_FIRST_NAME})")
    parser.add_argument("--last-name", dest="last_name", help=f"Last name (default: {DEFAULT_LAST_NAME})")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    success = create_admin_user(
        email=args.email,
        password=args.password,
        first_name=args.first_name,
        last_name=args.last_name,
    )
    if success:
        print("Admin user created/updated successfully.")
    else:
        print("Failed to create admin user.")
