
from flask import Flask
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

def update_admin_credentials():
    """Updates the admin user with the desired credentials and removes admin privileges from other accounts"""
    app = create_app()
    with app.app_context():
        try:
            # Set up the admin credentials
            admin_email = 'ryan@funlist.ai'
            admin_password = '120M2025*v7'
            
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
            
            # Remove admin privileges from other users
            other_admins = User.query.filter(User.email != admin_email, User.is_admin == True).all()
            
            if other_admins:
                for user in other_admins:
                    user.is_admin = False
                    logger.info(f"Removed admin privileges from: {user.email}")
            
            # Commit changes
            db.session.commit()
            
            # Verify the admin account
            admin = User.query.filter_by(email=admin_email).first()
            logger.info(f"Admin user confirmed:")
            logger.info(f"  ID: {admin.id}")
            logger.info(f"  Email: {admin.email}")
            logger.info(f"  Is Admin: {admin.is_admin}")
            logger.info(f"  Active: {admin.account_active}")
            
            return True
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating admin credentials: {str(e)}")
            return False

if __name__ == "__main__":
    success = update_admin_credentials()
    if success:
        print("Admin credentials updated successfully.")
        print("You can now log in as admin with:")
        print("Email: ryan@funlist.ai")
        print("Password: 120M2025*v7")
    else:
        print("Failed to update admin credentials.")
