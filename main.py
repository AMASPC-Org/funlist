import logging
import os
import signal
import subprocess
import time
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d',
    handlers=[logging.FileHandler('app.log'), logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Clean up existing processes using the ports we need
def kill_processes_on_port(port):
    try:
        # Find processes using the port
        result = subprocess.run(
            f"lsof -i :{port} -t", 
            shell=True, 
            capture_output=True, 
            text=True
        )
        pids = result.stdout.strip().split('\n')

        if pids and pids[0]:
            logger.info(f"Killing processes using port {port}: {', '.join(pids)}")
            for pid in pids:
                if pid:
                    try:
                        os.kill(int(pid), signal.SIGTERM)
                        logger.info(f"Successfully terminated process {pid}")
                    except Exception as e:
                        logger.error(f"Failed to kill process {pid}: {e}")
            # Give processes time to terminate
            time.sleep(1)
            return True
        return False
    except Exception as e:
        logger.error(f"Error managing processes on port {port}: {e}")
        return False

# Check and log port availability
def check_port_availability(ports):
    available_ports = []
    for port in ports:
        try:
            result = subprocess.run(
                f"lsof -i :{port} -t", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            if not result.stdout.strip():
                logger.info(f"Port {port} is available")
                available_ports.append(port)
            else:
                logger.info(f"Port {port} is in use")
        except Exception as e:
            logger.error(f"Error checking port {port}: {e}")
    return available_ports

# Kill processes on common ports we might use
kill_processes_on_port(8080)
kill_processes_on_port(5000)
kill_processes_on_port(3000)

# Check available ports
available_ports = check_port_availability([3000, 5000, 8080, 8081, 80])

logger.info("Starting Flask server...")
app = create_app()

# Preferred ports in order
preferred_ports = [5000, 3000, 8081, 8082, 4000, 5050, 7000]

if __name__ == "__main__":
    # Check if running in production/deployment environment
    if 'REPL_SLUG' in os.environ and os.environ.get('REPL_ENVIRONMENT') == 'production':
        # In production deployment, use port 80
        port = 80
        logger.info(f"Running in deployment environment. Starting server on port {port}...")
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # Use first available port from our preferred list
        port = int(os.environ.get('PORT', preferred_ports[0]))
        logger.info(f"Starting development server on port {port}...")

        # Try each port in sequence until one works
        for attempt_port in preferred_ports:
            try:
                logger.info(f"Attempting to start server on port {attempt_port}...")
                # Use 0.0.0.0 to make the server externally visible
                app.run(host='0.0.0.0', port=attempt_port, debug=True)
                break  # If we get here, the server started successfully
            except OSError as e:
                if "Address already in use" in str(e):
                    logger.warning(f"Port {attempt_port} is in use, trying next port...")
                    continue
                else:
                    logger.error(f"Error starting server on port {attempt_port}: {e}")
                    break
        else:
            logger.error("All ports are in use. Server could not be started.")