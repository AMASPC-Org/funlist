
from app import create_app
from models import User
from db_init import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_admin():
    app = create_app()
    with app.app_context():
        try:
            # Check for the admin user
            admin_email = 'ryan@americanmarketingalliance.com'
            admin = User.query.filter_by(email=admin_email).first()
            
            if admin:
                # Print admin user details
                logger.info(f"Admin user found:")
                logger.info(f"  ID: {admin.id}")
                logger.info(f"  Email: {admin.email}")
                logger.info(f"  Is Admin: {admin.is_admin}")
                logger.info(f"  Active: {admin.account_active}")
                
                # Check password
                test_password = '120M2025*v7'
                password_valid = admin.check_password(test_password)
                logger.info(f"  Password valid: {password_valid}")
                
                # Reset password and flags
                admin.set_password(test_password)
                admin.is_admin = True
                admin.account_active = True
                db.session.commit()
                logger.info("Admin account reset to default password and flagged as admin and active")
                
                # Verify changes
                admin = User.query.filter_by(email=admin_email).first()
                logger.info(f"Verification after update:")
                logger.info(f"  ID: {admin.id}")
                logger.info(f"  Email: {admin.email}")
                logger.info(f"  Is Admin: {admin.is_admin}")
                logger.info(f"  Active: {admin.account_active}")
                logger.info(f"  Password valid: {admin.check_password(test_password)}")
            else:
                logger.info(f"No admin user found with email {admin_email}")
                logger.info(f"Creating new admin user...")
                
                # Create new admin user
                new_admin = User(
                    email=admin_email,
                    is_admin=True,
                    account_active=True
                )
                new_admin.set_password(test_password)
                db.session.add(new_admin)
                db.session.commit()
                
                # Verify new admin
                admin = User.query.filter_by(email=admin_email).first()
                logger.info(f"New admin user created:")
                logger.info(f"  ID: {admin.id}")
                logger.info(f"  Email: {admin.email}")
                logger.info(f"  Is Admin: {admin.is_admin}")
                logger.info(f"  Active: {admin.account_active}")
                logger.info(f"  Password valid: {admin.check_password(test_password)}")
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error debugging admin: {str(e)}")
            raise

if __name__ == "__main__":
    debug_admin()
