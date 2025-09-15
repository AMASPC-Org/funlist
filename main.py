import logging
import os
import signal
import sys
import time
import socket
import subprocess
import psutil
import importlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def find_available_port(start_port=3000, max_attempts=15):
    """Find an available port starting from start_port."""
    port = start_port
    for _ in range(max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', port))
                s.listen(1)
                s.close()
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"Could not find an available port after {max_attempts} attempts")

def run_flask_app():
    """Run the Flask application."""
    try:
        # Force port 5000 to match workflow expectations
        preferred_port = 5000
        port = None
        
        # First check if preferred port is available
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('0.0.0.0', preferred_port))
                s.listen(1)
                s.close()
                port = preferred_port
            except OSError:
                # If preferred port is busy, find another available port
                port = find_available_port(5000)
                
        print(f"\033c", flush=True)  # Clear console
        print(f"Starting Flask server on port {port}")
        print(f"\n🚀 Server running at: http://0.0.0.0:{port}")
        if "REPL_SLUG" in os.environ and "REPL_OWNER" in os.environ:
            print(f"🌐 Public URL: https://{os.environ.get('REPL_SLUG')}.{os.environ.get('REPL_OWNER')}.repl.co")

        # Create and run the Flask app
        from app import create_app
        app = create_app()

        # Always bind to 0.0.0.0 to ensure the server is accessible externally
        app.run(
            host='0.0.0.0',
            port=port,
            debug=False,
            use_reloader=False,
            threaded=True
        )

    except Exception as e:
        logger.error(f"Error running Flask app: {str(e)}", exc_info=True)
        sys.exit(1)

def update_database_schema():
    try:
        # Import the database update function
        update_schema_module = importlib.import_module('update_schema')
        logger.info("Running database schema update...")
        result = update_schema_module.update_schema()
        if result:
            logger.info("Database schema updated successfully")
        else:
            logger.warning("Database schema update completed with warnings")
        return True
    except Exception as e:
        logger.error(f"Error updating database schema: {str(e)}")
        return False

# Create the Flask app
try:
    from app import create_app
    app = create_app()

    # Update database schema before starting
    update_database_schema()

    # Register signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}, shutting down")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
except Exception as e:
    logger.error(f"Error creating Flask app: {str(e)}", exc_info=True)
    sys.exit(1)

# Route definitions are handled in routes.py through init_routes
# Don't define routes here to avoid conflicts



if __name__ == "__main__":
    try:
        run_flask_app()
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        sys.exit(1)