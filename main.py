
import logging
import os
import signal
import subprocess
from app import create_app

# Kill any processes using port 8080 or 8081
def kill_port_processes(ports):
    for port in ports:
        try:
            # Find processes using the port
            result = subprocess.run(
                f"lsof -i :{port} -t", 
                shell=True, 
                capture_output=True, 
                text=True
            )
            pids = result.stdout.strip().split('\n')
            
            # Kill each process
            for pid in pids:
                if pid:
                    try:
                        os.kill(int(pid), signal.SIGKILL)
                        logging.info(f"Killed process {pid} using port {port}")
                    except ProcessLookupError:
                        pass
                    except Exception as e:
                        logging.error(f"Error killing process {pid}: {e}")
        except Exception as e:
            logging.error(f"Error checking port {port}: {e}")

# Clear any processes using our ports
kill_port_processes([8080, 8081])

logging.info("Starting Flask server...")
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
