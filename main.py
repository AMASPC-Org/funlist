import logging
import os
import signal
import subprocess
from app import create_app

# Log which ports are in use, but don't kill processes
def check_port_usage(ports):
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

            if pids and pids[0]:
                logging.info(f"Port {port} is in use by PIDs: {', '.join(pids)}")
                # Also list process details for debugging
                subprocess.run(f"ps -p {','.join(pids)} -o pid,ppid,cmd", shell=True)
            else:
                logging.info(f"Port {port} is available")
        except Exception as e:
            logging.error(f"Error checking port {port}: {e}")

# Check port availability without killing processes
check_port_usage([5000, 8081, 8080, 80])

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
        # In development, use port 5050 by default to avoid conflicts
        port = int(os.environ.get('PORT', 5050))
        print(f"Starting development server on port {port}...")

        # Try to start the server, with improved fallback port handling
        try:
            app.run(host='0.0.0.0', port=port, debug=True)
        except OSError as e:
            if "Address already in use" in str(e):
                # Try multiple fallback ports in sequence, prioritizing less commonly used ports
                fallback_ports = [5050, 4000, 4040, 4080, 6000, 7000]

                for fallback_port in fallback_ports:
                    print(f"Port {port} is in use. Attempting fallback on port {fallback_port}...")
                    try:
                        app.run(host='0.0.0.0', port=fallback_port, debug=True)
                        # If we get here, the server started successfully
                        break
                    except OSError as inner_e:
                        if "Address already in use" not in str(inner_e):
                            print(f"Error on fallback port {fallback_port}: {inner_e}")
                            break
                        print(f"Fallback port {fallback_port} also in use, trying next...")
                else:
                    print("All fallback ports are in use. Please manually stop running processes.")
            else:
                print(f"Error starting server: {e}")