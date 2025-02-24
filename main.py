
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
    default_port = 8080
    port = int(os.environ.get('PORT', default_port))
    
    # Try alternative ports if default is in use
    while is_port_in_use(port):
        port += 1
        if port > default_port + 10:  # Try up to 10 ports
            raise RuntimeError("No available ports found")
            
    print(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
