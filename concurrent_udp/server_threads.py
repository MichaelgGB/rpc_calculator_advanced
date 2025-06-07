# udp_concurrent/server_udp_concurrent_threads_rpc.py
import socket
import threading
from main_programs.rpc_logic import handle_rpc_request

HOST = '127.0.0.1'
PORT = 8000

def request_handler(data: bytes, addr, sock: socket.socket):
    """This function is executed in a new thread for each request."""
    print(f"[Thread for {addr}] processing request.")
    response_json = handle_rpc_request(data.decode('utf-8'))
    sock.sendto(response_json.encode('utf-8'), addr)

def run_server():
    """Binds the main socket and spawns a new thread for each datagram."""
    
    # --- START OF FIX: Use a shutdown flag ---
    shutdown_flag = threading.Event()
    # --- END OF FIX ---

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        s.settimeout(1.0)
        
        print(f"Concurrent UDP RPC Server (Threads) listening on {HOST}:{PORT}")
        print("Press Ctrl+C to shut down.")
        
        # --- START OF FIX: Main loop checks the flag ---
        while not shutdown_flag.is_set():
            try:
                data, addr = s.recvfrom(1024)
                
                thread = threading.Thread(target=request_handler, args=(data, addr, s))
                thread.daemon = True 
                thread.start()
                
            except socket.timeout:
                # This is normal, allows the loop to check the shutdown_flag
                continue
            except KeyboardInterrupt:
                # Catch Ctrl+C to set the flag and break the loop
                print("\nShutdown signal received...")
                shutdown_flag.set()
        # --- END OF FIX ---

    print("Server has shut down gracefully.")

if __name__ == "__main__":
    run_server()