import os
import logging
from app import create_app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        app = create_app()
        logger.info("Starting Flask server on port 3000")
        app.run(host='0.0.0.0', port=3000, debug=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise