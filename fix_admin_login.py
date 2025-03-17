
from flask import Flask
from werkzeug.security import generate_password_hash
import os
from db_init import db
from models import User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///instance/funlist.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def fix_admin_login():
    """Creates or updates the admin user with expected credentials"""
    app = create_app()
    with app.app_context():
        try:
            # The email that the routes.py admin_login route is expecting
            admin_email = 'ryan@funlist.ai'
            admin_password = 'admin123'  # Using a simple password for testing
            
            # Check if admin exists
            admin = User.query.filter_by(email=admin_email).first()
            
            if admin:
                # Update existing admin
                admin.set_password(admin_password)
                admin.is_admin = True
                admin.account_active = True
                logger.info(f"Updated admin user: {admin_email}")
            else:
                # Create new admin
                admin = User(
                    email=admin_email,
                    is_admin=True,
                    account_active=True
                )
                admin.set_password(admin_password)
                db.session.add(admin)
                logger.info(f"Created new admin user: {admin_email}")
            
            # Also ensure your test admin has admin privileges
            test_admin = User.query.filter_by(email='admin@example.com').first()
            if test_admin:
                test_admin.is_admin = True
                test_admin.account_active = True
                logger.info("Updated test admin permissions")
            
            # Commit changes
            db.session.commit()
            
            # Verify admin exists
            admin = User.query.filter_by(email=admin_email).first()
            if admin:
                logger.info(f"Admin user confirmed:")
                logger.info(f"  ID: {admin.id}")
                logger.info(f"  Email: {admin.email}")
                logger.info(f"  Is Admin: {admin.is_admin}")
                logger.info(f"  Active: {admin.account_active}")
                return True
            else:
                logger.error("Failed to verify admin user after update/creation")
                return False
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in fix_admin_login: {str(e)}")
            return False

if __name__ == "__main__":
    success = fix_admin_login()
    if success:
        print("Admin account fixed successfully.")
        print("You can now log in as admin with:")
        print("Email: ryan@funlist.ai")
        print("Password: admin123")
    else:
        print("Failed to fix admin account.")
