
import socket
import psutil
import os

def check_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
            s.listen(1)
            s.close()
            return False
        except OSError:
            return True

def find_process_using_port(port):
    """Find the process ID using a given port"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port:
                    return proc
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return None

def main():
    """Check ports used by the application"""
    ports_to_check = [3000, 8080]
    
    print("Checking ports used by the application...")
    for port in ports_to_check:
        in_use = check_port_in_use(port)
        print(f"Port {port}: {'In use' if in_use else 'Available'}")
        
        if in_use:
            proc = find_process_using_port(port)
            if proc:
                print(f"  Used by: PID {proc.pid} - {proc.name()} - {' '.join(proc.cmdline())}")
            else:
                print(f"  Could not determine which process is using port {port}")

if __name__ == "__main__":
    main()
