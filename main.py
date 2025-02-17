
import logging
import socket
from app import app

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        port = 8080
        logger.info(f"Starting server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}", exc_info=True)
