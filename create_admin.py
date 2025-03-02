
import os
import sys
from flask import Flask
from models import User
from db_init import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def create_admin_user():
    app = create_app()
    with app.app_context():
        try:
            # Check if admin user already exists
            admin_email = 'ryan@americanmarketingalliance.com'
            admin_password = '120M2025*v7'
            
            admin = User.query.filter_by(email=admin_email).first()
            if admin:
                logger.info(f"Admin user already exists: {admin_email}")
                admin.is_admin = True
                admin.is_subscriber = True
                admin.is_event_creator = True
                admin.is_organizer = True
                admin.account_active = True
                admin.set_password(admin_password)
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
                    account_active=True
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

if __name__ == "__main__":
    success = create_admin_user()
    if success:
        print("Admin user created/updated successfully.")
    else:
        print("Failed to create admin user.")
