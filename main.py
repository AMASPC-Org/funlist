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

def is_port_in_use(port):
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return False
        except socket.error:
            return True

if __name__ == "__main__":
    port = 8080
    max_retries = 3

    for retry in range(max_retries):
        if not is_port_in_use(port):
            logger.info(f"Starting server on port {port}")
            try:
                app.run(host='0.0.0.0', port=port, debug=True)
                break
            except Exception as e:
                logger.error(f"Failed to start server: {e}", exc_info=True)
        else:
            print(f"Port {port} is in use, trying port {port + 1}")
            port += 1
    else:
        print(f"Could not find available port after {max_retries} attempts")