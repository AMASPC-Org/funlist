import logging
import os
import signal
import sys
import time
import socket
import subprocess
import psutil

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
    preferred_ports = [3000, 5000, 8080, 8081]
    port = int(os.environ.get("PORT", preferred_ports[0]))

    # Check each port and try to free it if needed
    for current_port in preferred_ports:
        if is_port_in_use(current_port):
            logger.info(f"Port {current_port} is in use, attempting to free it")
            if free_port(current_port):
                logger.info(f"Successfully freed port {current_port}")
                port = current_port
                break
        else:
            logger.info(f"Port {current_port} is available")
            port = current_port
            break

    # Create and run the Flask app
    from app import create_app
    app = create_app()

    # Register signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}, shutting down")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False, threaded=True)

if __name__ == "__main__":
    try:
        run_flask_app()
    except Exception as e:
        logger.error(f"Fatal error in main: {e}", exc_info=True)
        sys.exit(1)