
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
        # Kill any existing processes on our ports
        ports = [5006, 3000, 8080, 8000]
        app = create_app()
        
        for port in ports:
            try:
                logger.info(f"Starting Flask server on port {port}")
                app.run(host='0.0.0.0', port=port, debug=True)
                break
            except OSError:
                if port == ports[-1]:
                    raise
                logger.warning(f"Port {port} is in use, trying next port")
                continue
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
