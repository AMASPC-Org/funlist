
from app import create_app
import os
import socket
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return False
        except OSError:
            return True

app = create_app()

if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5006))
        logger.info(f"Attempting to start server on port {port}")
        
        if is_port_in_use(port):
            logger.warning(f"Port {port} is in use, trying alternative ports")
            for new_port in range(port + 1, port + 10):
                if not is_port_in_use(new_port):
                    port = new_port
                    break
            else:
                raise RuntimeError("No available ports found")
        
        logger.info(f"Starting server on port {port}")
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            threaded=True,
            use_reloader=False
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
