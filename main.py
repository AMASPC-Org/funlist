
import logging
import psutil
from app import app

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def check_port_usage(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            logger.warning(f"Port {port} is already in use by PID {conn.pid}")
            return True
    return False

if __name__ == "__main__":
    port = 8080
    logger.info(f"Attempting to start server on port {port}")
    
    if check_port_usage(port):
        logger.error(f"Port {port} is already in use")
    else:
        logger.info(f"Port {port} is available")
        
    try:
        app.run(host="0.0.0.0", port=port, debug=True)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}", exc_info=True)
