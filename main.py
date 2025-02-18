
import os
import logging
from flask import Flask

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    from app import create_app as init_app
    return init_app()

if __name__ == "__main__":
    try:
        app = create_app()
        default_ports = [5006, 3000, 8000, 8080]
        
        for port in default_ports:
            try:
                logger.info(f"Attempting to start Flask server on port {port}")
                app.run(host='0.0.0.0', port=port, debug=True)
                break
            except OSError as e:
                logger.warning(f"Port {port} is in use, trying next port")
                continue
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
