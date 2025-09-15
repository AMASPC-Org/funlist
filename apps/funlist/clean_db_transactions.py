
import logging
from sqlalchemy import text
from db_init import db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_transactions():
    """Clean up any lingering database transactions."""
    try:
        logger.info("Starting database transaction cleanup")
        
        # Close all connections in the pool
        db.engine.dispose()
        
        # Create a new connection
        with db.engine.connect() as conn:
            # Roll back any open transactions
            conn.execute(text("ROLLBACK"))
            
            # Cancel any queries that might be hanging
            try:
                conn.execute(text("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'idle in transaction'"))
            except Exception as e:
                logger.warning(f"Could not terminate idle transactions: {str(e)}")
            
            conn.commit()
        
        logger.info("Database transaction cleanup complete")
        return True
    except Exception as e:
        logger.error(f"Error during database cleanup: {str(e)}")
        return False

if __name__ == "__main__":
    clean_transactions()
    logger.info("Done")
