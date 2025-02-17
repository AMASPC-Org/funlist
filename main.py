
import logging
import socket
from app import app

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def find_available_port(start_port, max_retries=3):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_retries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                return port
            except socket.error:
                logger.warning(f"Port {port} is in use, trying next port")
                continue
    raise RuntimeError(f"Could not find available port after {max_retries} attempts")

if __name__ == "__main__":
    try:
        # Try to start with preferred port
        preferred_port = int(app.config.get('PORT', 8080))
        port = find_available_port(preferred_port)
        
        logger.info(f"Starting server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}", exc_info=True)
