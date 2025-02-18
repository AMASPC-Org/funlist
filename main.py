
import logging
from flask import Flask
from app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("Starting Flask server on port 8080...")
        app.run(
            host='0.0.0.0',
            port=8080,
            debug=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
