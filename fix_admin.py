
from flask import Flask
from models import User
from db_init import db
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_admin_user():
    # Import app here to avoid circular imports
    from app import create_app
    app = create_app()
    
    with app.app_context():
        try:
            # Check all existing users
            all_users = User.query.all()
            logger.info(f"Found {len(all_users)} users in the database.")
            
            # Find users with the admin email
            admin_email = 'ryan@americanmarketingalliance.com'
            admin_users = User.query.filter_by(email=admin_email).all()
            
            if len(admin_users) > 1:
                # Multiple users with admin email found - keep only one
                logger.warning(f"Found {len(admin_users)} users with email {admin_email}. Keeping only one.")
                primary_admin = admin_users[0]
                primary_admin.is_admin = True
                primary_admin.account_active = True
                primary_admin.set_password('120M2025*v7')
                
                # Delete the duplicates
                for other_admin in admin_users[1:]:
                    logger.info(f"Deleting duplicate admin user ID: {other_admin.id}")
                    db.session.delete(other_admin)
                
                db.session.commit()
                logger.info("Duplicates removed, primary admin account updated.")
            elif len(admin_users) == 1:
                # One user found - make sure it's set as admin
                admin = admin_users[0]
                if not admin.is_admin:
                    logger.info(f"User ID: {admin.id} found with email {admin_email} but not marked as admin. Fixing...")
                    admin.is_admin = True
                    admin.account_active = True
                    admin.set_password('120M2025*v7')
                    db.session.commit()
                    logger.info("Admin account updated.")
                else:
                    logger.info(f"Admin user ID: {admin.id} is already set up correctly.")
            else:
                # No admin found - create one
                logger.info(f"No user found with email {admin_email}. Creating new admin account.")
                admin = User(
                    email=admin_email,
                    is_admin=True,
                    account_active=True
                )
                admin.set_password('120M2025*v7')
                db.session.add(admin)
                db.session.commit()
                logger.info("New admin account created.")
            
            # Verify the fix
            admin = User.query.filter_by(email=admin_email).first()
            if admin and admin.is_admin:
                logger.info(f"Verification successful - Admin user ID: {admin.id}, is_admin: {admin.is_admin}")
                return True
            else:
                logger.error("Admin verification failed!")
                return False
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error fixing admin: {str(e)}")
            raise

if __name__ == '__main__':
    fix_admin_user()
