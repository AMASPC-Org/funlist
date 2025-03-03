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

def is_port_in_use(port):
    """Check if a port is in use using socket."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('0.0.0.0', port)) == 0

def find_process_on_port(port):
    """Find process using a specific port using psutil."""
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                for conn in proc.connections(kind='inet'):
                    if conn.laddr.port == port:
                        return proc.pid
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
    except Exception as e:
        logger.error(f"Error finding process on port {port}: {e}")
    return None

def terminate_process(pid):
    """Terminate a process by PID."""
    if not pid:
        return False

    try:
        process = psutil.Process(pid)
        logger.info(f"Terminating process {pid} ({process.name()})")
        process.terminate()

        # Wait for termination
        gone, alive = psutil.wait_procs([process], timeout=3)
        if process in alive:
            logger.info(f"Process {pid} did not terminate, sending SIGKILL")
            process.kill()

        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
        logger.error(f"Error terminating process {pid}: {e}")
        return False

def free_port(port):
    """Free a port by terminating the process using it."""
    if not is_port_in_use(port):
        logger.info(f"Port {port} is already free")
        return True

    pid = find_process_on_port(port)
    if pid:
        logger.info(f"Found process {pid} using port {port}")
        return terminate_process(pid)
    else:
        # Try lsof as a backup
        try:
            cmd = f"lsof -i :{port} -t"
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()
            if output:
                for pid_str in output.split('\n'):
                    try:
                        terminate_process(int(pid_str))
                    except ValueError:
                        continue
                return not is_port_in_use(port)
        except subprocess.SubprocessError:
            pass

    # Last resort: pkill
    try:
        subprocess.run(['pkill', '-f', f':{port}'], check=False)
        time.sleep(1)
        return not is_port_in_use(port)
    except Exception as e:
        logger.error(f"Error using pkill: {e}")

    return False

def run_flask_app():
    """Run the Flask application on the appropriate port."""
    # Get the preferred port from environment or use default
    preferred_ports = [5000, 3000, 8081, 8080]  # Changed order to prioritize 5000
    port = int(os.environ.get("PORT", preferred_ports[0]))
    
    # Try to find an available port
    available_port = None
    for current_port in preferred_ports:
        if not is_port_in_use(current_port):
            logger.info(f"Port {current_port} is available")
            available_port = current_port
            break
        else:
            logger.info(f"Port {current_port} is in use")
    
    # If no ports are available, try to free one
    if available_port is None:
        for current_port in preferred_ports:
            logger.info(f"Attempting to free port {current_port}")
            if free_port(current_port):
                logger.info(f"Successfully freed port {current_port}")
                available_port = current_port
                break
    
    # If we still don't have a port, use a fallback
    if available_port is None:
        available_port = 5050  # Use an uncommon port as last resort
        logger.warning(f"Using fallback port {available_port}")
    
    port = available_port
    logger.info(f"Selected port {port} for the application")

    # Update database schema function
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


    try:
        logger.info(f"Starting Flask server on port {port}")
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start Flask server: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    try:
        run_flask_app()
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        sys.exit(1)