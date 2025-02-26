
from app import app
from models import User
from db_init import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_admin():
    with app.app_context():
        try:
            # Check if admin already exists
            admin = User.query.filter_by(email='ryan@americanmarketingalliance.com').first()
            
            admin_password = '120M2025*v7'
            
            if not admin:
                # Create new admin
                logger.info("Creating new admin user...")
                admin = User(
                    email='ryan@americanmarketingalliance.com',
                    is_admin=True,
                    account_active=True
                )
                admin.set_password(admin_password)
                db.session.add(admin)
                db.session.commit()
                logger.info("Admin user created successfully")
            else:
                # Update existing admin
                logger.info(f"Updating existing admin (ID: {admin.id})...")
                admin.is_admin = True
                admin.account_active = True
                admin.set_password(admin_password)
                db.session.commit()
                logger.info("Admin user updated successfully")
            
            # Verify admin creation/update
            admin = User.query.filter_by(email='ryan@americanmarketingalliance.com').first()
            if admin:
                logger.info(f"Admin verification - ID: {admin.id}, is_admin: {admin.is_admin}, active: {admin.account_active}")
                pwd_check = admin.check_password(admin_password)
                logger.info(f"Password verification result: {pwd_check}")
                
                if not admin.is_admin:
                    logger.error("ERROR: Admin flag not set!")
                if not admin.account_active:
                    logger.error("ERROR: Admin account not active!")
                if not pwd_check:
                    logger.error("ERROR: Password verification failed!")
            else:
                logger.error("ERROR: Admin user not found after creation/update!")
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating/updating admin: {str(e)}")
            raise

if __name__ == '__main__':
    create_admin()
