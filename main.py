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
        # Kill any existing processes on common ports first
        for port_to_check in [8080, 5000, 3000]:
            try:
                for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                    try:
                        for conn in proc.net_connections():
                            if conn.laddr.port == port_to_check:
                                logger.info(f"Killing process {proc.pid} using port {port_to_check}")
                                proc.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except Exception as e:
                logger.debug(f"Error checking port {port_to_check}: {e}")
        
        time.sleep(1)  # Give processes time to release ports
        
        # Always use port 5000 for Replit
        port = 5000
        
        # Log the effective OAuth callback URL
        app_url = os.environ.get('APP_URL', 'https://<your-repl>.replit.dev')
        print(f"\n{'='*60}")
        print(f"Starting Flask server on port {port}")
        print(f"🚀 Server running at: http://0.0.0.0:{port}")
        print(f"📋 Google OAuth Redirect URI: {app_url}/google_login/callback")
        print(f"{'='*60}\n")

        # Update database schema first (before creating app)
        update_database_schema()

        # Create and run the Flask app
        from app import create_app
        app = create_app()

        # Bind to 0.0.0.0 for external access
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

# Don't create app globally - do it in run_flask_app() only
app = None

if __name__ == "__main__":
    # Register signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}, shutting down")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        run_flask_app()
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        sys.exit(1)