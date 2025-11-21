
from flask import Flask
from db_init import db
from models import User
import logging

from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = settings.get("DATABASE_URL", "sqlite:///instance/funlist.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    return app

def ensure_single_admin():
    """Ensures ryan@funlist.ai is the only admin in the system"""
    app = create_app()
    with app.app_context():
        try:
            # Ensure the primary admin exists and has admin privileges
            admin_email = 'ryan@funlist.ai'
            admin = User.query.filter_by(email=admin_email).first()
            
            if admin:
                # Make sure this user has admin privileges
                admin.is_admin = True
                admin.account_active = True
                logger.info(f"Verified admin user: {admin_email}")
            else:
                # This shouldn't happen as we've already fixed it, but just in case
                logger.error(f"Primary admin {admin_email} not found in the database!")
                return False
            
            # Remove admin privileges from all other users
            other_admins = User.query.filter(User.email != admin_email, User.is_admin == True).all()
            
            if other_admins:
                for user in other_admins:
                    user.is_admin = False
                    logger.info(f"Removed admin privileges from: {user.email}")
            
            # Commit changes
            db.session.commit()
            
            # Verify changes
            current_admins = User.query.filter_by(is_admin=True).all()
            if len(current_admins) == 1 and current_admins[0].email == admin_email:
                logger.info(f"Success: {admin_email} is now the only admin in the system")
                return True
            else:
                admin_emails = [user.email for user in current_admins]
                logger.error(f"Failed to ensure single admin. Current admins: {admin_emails}")
                return False
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in ensure_single_admin: {str(e)}")
            return False

if __name__ == "__main__":
    success = ensure_single_admin()
    if success:
        print(f"Successfully configured ryan@funlist.ai as the only admin in the system.")
    else:
        print("Failed to configure single admin. Check the logs for details.")
