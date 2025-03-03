
import logging
import os
import signal
import subprocess
from app import create_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check if a port is in use
def check_port(port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('0.0.0.0', port))
    sock.close()
    return result == 0

# Function to find processes using a port
def find_processes_using_port(port):
    try:
        # Use lsof command to find processes using the port
        cmd = f"lsof -i :{port} -t"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        if output:
            pids = output.split('\n')
            # Get process details
            process_info = []
            for pid in pids:
                try:
                    cmd = f"ps -p {pid} -o pid,ppid,cmd"
                    process_detail = subprocess.check_output(cmd, shell=True).decode()
                    process_info.append(process_detail)
                except:
                    pass
            return pids, '\n'.join(process_info)
        return [], ""
    except:
        return [], ""

# Check various ports
for port in [5000, 8081, 8080, 80]:
    if check_port(port):
        pids, process_info = find_processes_using_port(port)
        logger.info(f"Port {port} is in use by PIDs: {', '.join(pids)}")
        logger.info(process_info)
    else:
        logger.info(f"Port {port} is available")

# Use the PORT environment variable (for Replit) or default to 3000
port = int(os.environ.get("PORT", 3000))
logger.info(f"Starting Flask server...")

# Kill any existing processes using port 3000 (our target port)
def kill_processes_on_port(port):
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        logger.info(f"Killing process {proc.pid} {proc.name()} using port {port}")
                        proc.kill()
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except ImportError:
        logger.warning("psutil not available, using lsof to kill processes")
        try:
            import os
            os.system(f"pkill -f 'python.*main.py'")
            return True
        except Exception as e:
            logger.error(f"Error killing processes: {e}")
    return False

# Create the Flask app
app = create_app()
if __name__ == "__main__":
    # First try to kill any existing processes
    kill_processes_on_port(port)
    
    # Try to run on the specified port, fall back to other ports if needed
    max_port_tries = 10
    current_port = port
    
    for attempt in range(max_port_tries):
        try:
            logger.info(f"Attempting to start server on port {current_port}...")
            app.run(host='0.0.0.0', port=current_port, debug=True)
            break
        except OSError as e:
            if "Address already in use" in str(e):
                logger.warning(f"Port {current_port} is already in use, trying next port")
                current_port += 1
                if attempt == max_port_tries - 1:
                    logger.error(f"Could not find an available port after {max_port_tries} attempts")
                    raise
            else:
                logger.error(f"Error starting server: {e}")
                raise
