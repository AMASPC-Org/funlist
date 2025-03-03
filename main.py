
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

# Create and run the Flask app
app = create_app()
if __name__ == "__main__":
    # Run the app with the appropriate host and port
    app.run(host='0.0.0.0', port=port, debug=True)
