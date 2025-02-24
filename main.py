
from app import create_app
import os
import socket

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            return False
        except OSError:
            return True

app = create_app()

if __name__ == '__main__':
    port = 8080  # Default port for Replit webview
    
    # Try alternative ports if default is in use
    while is_port_in_use(port):
        port += 1
        if port > 8090:  # Try up to port 8090
            raise RuntimeError("No available ports found")
            
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
