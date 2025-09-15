
import os
import sys
from app import create_app
from db_init import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_database_sessions():
    """Clean up any stale database sessions and fix transaction state."""
    logger.info("Fixing database sessions...")
    
    app = create_app()
    with app.app_context():
        try:
            # Close any existing sessions
            db.session.remove()
            
            # Execute a raw SQL command to terminate any in-progress transactions
            db.session.execute("ROLLBACK")
            db.session.commit()
            
            # Test a simple query to verify database is now accessible
            result = db.session.execute("SELECT 1").fetchone()
            if result and result[0] == 1:
                logger.info("Database connection successful.")
            else:
                logger.error("Database connection test failed.")
                return False
                
            logger.info("Database sessions fixed successfully.")
            return True
        except Exception as e:
            logger.error(f"Error fixing database sessions: {str(e)}")
            return False

if __name__ == "__main__":
    success = fix_database_sessions()
    sys.exit(0 if success else 1)
