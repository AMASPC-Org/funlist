
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
        # Try ports in sequence until one works
        ports = [8000, 8080, 3000, 5000]  # Changed port order
        started = False
        
        for port in ports:
            try:
                logger.info(f"Attempting to start Flask server on port {port}")
                app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)  # Disabled reloader
                started = True
                break
            except OSError as e:
                logger.warning(f"Port {port} is in use, trying next port")
                continue
                
        if not started:
            logger.error("Could not find an available port")
            raise RuntimeError("No ports available")
            
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise
