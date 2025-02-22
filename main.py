
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
        port = 5006
        logger.info(f"Starting server on port {port}")
        app.run(
            host='0.0.0.0',
            port=port,
            debug=True,
            threaded=True,
            use_reloader=False
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
