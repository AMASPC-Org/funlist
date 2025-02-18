import os
import logging
from app import create_app  # Import the create_app function

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        ports = [5006, 3000, 8080, 8000]
        for port in ports:
            try:
                app = create_app()
                logger.info(f"Starting Flask server on port {port}")
                app.run(host='0.0.0.0', port=port, debug=True)
                break
            except OSError:
                logger.warning(f"Port {port} is in use, trying next port")
                continue
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise