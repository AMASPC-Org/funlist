import os
import logging
from app import create_app  # Import the create_app function

# Configure logging (basicConfig is fine for simple cases)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Get the port from the environment variable (set in .replit)
        port = int(os.environ.get("PORT", 5006))  # Default to 5006 if PORT is not set
        logger.info(f"Starting Flask server on port {port}")

        # Create the Flask app using the factory function
        app = create_app()
        app.run(host='0.0.0.0', port=port, debug=True)  # Run the app
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise