
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
    # Check if running in production/deployment environment
    if 'REPL_SLUG' in os.environ and os.environ.get('REPL_ENVIRONMENT') == 'production':
        # In production deployment, use port 80
        port = 80
        print(f"Running in deployment environment. Starting server on port {port}...")
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # In development, try ports in sequence
        ports_to_try = [8080, 5000, 3000, 5006, 8000]
        
        for port in ports_to_try:
            try:
                print(f"Starting development server on port {port}...")
                app.run(host='0.0.0.0', port=port, debug=True)
                break  # Exit the loop if server starts successfully
            except OSError as e:
                if "Address already in use" in str(e):
                    print(f"Port {port} is already in use, trying another port...")
                else:
                    print(f"Error starting server: {e}")
                    raise
        else:
            print("Could not find an available port. Please check your running processes.")
