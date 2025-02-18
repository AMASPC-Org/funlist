
import os
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
        port = 5006  # Set fixed port for consistency
        logger.info(f"Starting Flask server on port {port}...")
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            port=port,
            debug=False
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
