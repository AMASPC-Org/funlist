
import logging
import os
import signal
import subprocess
import time
import sys
from app import create_app

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def check_port_availability(port):
    """Check if a port is available for use."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', port))
        available = True
    except socket.error:
        available = False
    finally:
        sock.close()
    return available

def find_process_using_port(port):
    """Find PIDs of processes using a specific port using multiple methods."""
    processes = set()
    
    # Try psutil first if available
    try:
        import psutil
        for conn in psutil.net_connections(kind='inet'):
            if hasattr(conn, 'laddr') and hasattr(conn.laddr, 'port') and conn.laddr.port == port:
                if conn.pid is not None:
                    processes.add(conn.pid)
        logger.info(f"Found {len(processes)} processes using port {port} via psutil")
    except (ImportError, AttributeError) as e:
        logger.warning(f"Could not use psutil to find processes: {e}")
    
    # Also try lsof as a backup
    try:
        cmd = f"lsof -i :{port} -t"
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode().strip()
        if output:
            for pid in output.split('\n'):
                processes.add(int(pid))
            logger.info(f"Found {len(processes)} processes using port {port} via lsof")
    except (subprocess.SubprocessError, ValueError) as e:
        logger.warning(f"Could not use lsof to find processes: {e}")
        
    return list(processes)

def kill_process(pid):
    """Kill a process by PID, trying SIGTERM first, then SIGKILL if needed."""
    try:
        # Try killing gracefully first
        os.kill(pid, signal.SIGTERM)
        logger.info(f"Sent SIGTERM to process {pid}")
        
        # Wait a moment to see if it terminates
        time.sleep(0.5)
        
        # Check if process still exists
        try:
            os.kill(pid, 0)  # This will raise an error if process doesn't exist
            # Process still exists, use SIGKILL
            logger.warning(f"Process {pid} did not terminate with SIGTERM, using SIGKILL")
            os.kill(pid, signal.SIGKILL)
            return True
        except OSError:
            # Process has already terminated
            return True
    except OSError as e:
        logger.error(f"Failed to kill process {pid}: {e}")
        return False

def free_port(port):
    """Free up a port by killing all processes using it."""
    pids = find_process_using_port(port)
    
    if not pids:
        logger.info(f"No processes found using port {port}")
        return True
    
    logger.info(f"Attempting to kill {len(pids)} processes using port {port}")
    
    success = True
    for pid in pids:
        if not kill_process(pid):
            success = False
    
    # Verify the port is now available
    if check_port_availability(port):
        logger.info(f"Successfully freed port {port}")
        return True
    else:
        logger.warning(f"Port {port} is still in use after killing processes")
        
        # Last resort: try pkill command
        try:
            subprocess.run(['pkill', '-f', f':{port}'], check=False)
            time.sleep(1)
            
            if check_port_availability(port):
                logger.info(f"Successfully freed port {port} using pkill")
                return True
        except Exception as e:
            logger.error(f"Error using pkill: {e}")
        
        return False

def run_flask_app(app, host='0.0.0.0', preferred_port=3000, max_attempts=5):
    """Run the Flask app with automatic port selection."""
    port = preferred_port
    
    # Check several common ports for availability
    for check_port in [3000, 5000, 8080, 8081]:
        available = check_port_availability(check_port)
        logger.info(f"Port {check_port} is {'available' if available else 'in use'}")
    
    for attempt in range(max_attempts):
        if not check_port_availability(port):
            logger.info(f"Port {port} is in use, attempting to free it")
            if not free_port(port):
                logger.warning(f"Could not free port {port}, trying next port")
                port += 1
                continue
                
        try:
            logger.info(f"Starting Flask application on http://{host}:{port}")
            app.run(
                host=host,
                port=port,
                debug=True,
                use_reloader=False,
                threaded=True
            )
            # If we get here without an exception, the app started successfully
            return True
        except OSError as e:
            if "Address already in use" in str(e):
                logger.warning(f"Port {port} is still in use despite our checks. Trying port {port+1}")
                port += 1
            else:
                logger.error(f"Failed to start Flask app: {e}")
                return False
    
    logger.error(f"Could not find an available port after {max_attempts} attempts")
    return False

if __name__ == "__main__":
    # Use environment variable PORT if available
    port = int(os.environ.get("PORT", 3000))
    
    # Create Flask app
    try:
        app = create_app()
        logger.info("Flask app created successfully")
        
        # Set explicit error handler for SIGTERM to log shutdown
        def handle_sigterm(signum, frame):
            logger.info("Received SIGTERM signal, shutting down gracefully")
            sys.exit(0)
        
        signal.signal(signal.SIGTERM, handle_sigterm)
        
        # Run the app
        if not run_flask_app(app, preferred_port=port):
            logger.error("Failed to start Flask application")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        sys.exit(1)
