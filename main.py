
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
            else:
                logging.info(f"Port {port} is available")
        except Exception as e:
            logging.error(f"Error checking port {port}: {e}")

# Check port availability without killing processes
check_port_usage([8080, 8081, 5000, 80])

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
        # In development, use PORT from environment or default to 8080
        port = int(os.environ.get('PORT', 8080))
        print(f"Starting development server on port {port}...")
        
        # Try to start the server, with clearer error handling
        try:
            app.run(host='0.0.0.0', port=port, debug=True)
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"ERROR: Port {port} is already in use. Please try:")
                print(f"  1. Wait a moment for the previous server to shut down")
                print(f"  2. Or edit .replit to use a different port")
                
                # Try one alternate port as a fallback
                fallback_port = 5000
                print(f"Attempting fallback on port {fallback_port}...")
                try:
                    app.run(host='0.0.0.0', port=fallback_port, debug=True)
                except:
                    print(f"Fallback port {fallback_port} also failed.")
            else:
                print(f"Error starting server: {e}")
