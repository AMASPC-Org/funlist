
#!/usr/bin/env python3
from app import create_app
from models import User
from db_init import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_users():
    """Remove all users except the admin (ryan@funlist.ai)"""
    app = create_app()
    with app.app_context():
        try:
            # Keep track of how many users will be deleted
            admin_email = 'ryan@funlist.ai'
            admin = User.query.filter_by(email=admin_email).first()
            
            if not admin:
                logger.error(f"Admin user '{admin_email}' not found in database.")
                return False
                
            # Count users before deletion
            total_users = User.query.count()
            
            # Delete all users except admin
            deleted = User.query.filter(User.email != admin_email).delete()
            
            # Commit changes
            db.session.commit()
            
            logger.info(f"Successfully kept admin user: {admin_email}")
            logger.info(f"Removed {deleted} user(s) from database")
            logger.info(f"Database now has {total_users - deleted} user(s)")
            
            return True
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error resetting users: {str(e)}")
            return False

if __name__ == "__main__":
    success = reset_users()
    print("Database reset completed successfully" if success else "Database reset failed")
