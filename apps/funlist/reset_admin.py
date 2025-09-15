
from app import create_app
from models import User
from db_init import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def reset_admin():
    app = create_app()
    with app.app_context():
        try:
            # Find the admin user
            admin_email = 'ryan@americanmarketingalliance.com'
            user = User.query.filter_by(email=admin_email).first()
            
            if user:
                logger.info(f"Found user: {user.id} with email {user.email}")
                # Reset password and ensure admin privileges
                user.set_password('120M2025*v7')
                user.is_admin = True
                user.account_active = True
                db.session.commit()
                logger.info("Admin password and privileges reset successfully")
                logger.info(f"Updated user: ID: {user.id}, Email: {user.email}, is_admin: {user.is_admin}, active: {user.account_active}")
                
                # Verify password
                verify = user.check_password('120M2025*v7')
                logger.info(f"Password verification result: {verify}")
            else:
                logger.warning(f"No user found with email {admin_email}. Creating new admin.")
                new_admin = User(
                    email=admin_email,
                    is_admin=True,
                    account_active=True
                )
                new_admin.set_password('120M2025*v7')
                db.session.add(new_admin)
                db.session.commit()
                logger.info(f"Created new admin user: ID: {new_admin.id}")
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error resetting admin: {e}")

if __name__ == "__main__":
    reset_admin()
