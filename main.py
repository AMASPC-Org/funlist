
import os
import logging
from app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 8080))
        retries = 3
        while retries > 0:
            try:
                logger.info(f"Attempting to start Flask server on port {port}...")
                app.run(host='0.0.0.0', port=port, debug=True)
                break
            except OSError as e:
                if "Address already in use" in str(e):
                    logger.warning(f"Port {port} is in use, trying port {port + 1}")
                    port += 1
                    retries -= 1
                else:
                    raise
        if retries == 0:
            logger.error("Could not find an available port")
            raise RuntimeError("No available ports found")
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
