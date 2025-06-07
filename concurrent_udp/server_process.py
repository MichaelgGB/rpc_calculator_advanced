# udp_concurrent/server_udp_concurrent_processes_rpc.py
import socket
import multiprocessing
from main_programs.rpc_logic import handle_rpc_request

HOST = '127.0.0.1'
PORT = 8000

def request_handler(data: bytes, addr):
    """This function is executed in a new process for each request."""
    process_name = multiprocessing.current_process().name
    print(f"[{process_name} for {addr}] processing request.")
    response_json = handle_rpc_request(data.decode('utf-8'))
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as reply_socket:
        reply_socket.sendto(response_json.encode('utf-8'), addr)

def run_server():
    """Binds the main socket and spawns a new process for each datagram."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        
        # --- START OF FIX: Set a timeout on the socket ---
        s.settimeout(1.0)
        # --- END OF FIX ---
        
        print(f"Concurrent UDP RPC Server (Processes) listening on {HOST}:{PORT}")
        print("Press Ctrl+C to shut down.")
        
        try:
            while True:
                try:
                    # This call will now unblock after 1 second.
                    data, addr = s.recvfrom(1024)
                    
                    process = multiprocessing.Process(target=request_handler, args=(data, addr))
                    process.start()
                    
                except socket.timeout:
                    # When the timeout occurs, we loop again, giving Python
                    # a chance to process the KeyboardInterrupt if it was pressed.
                    continue
                    
        except KeyboardInterrupt:
            print("\nShutdown signal received. Server is closing gracefully.")

if __name__ == "__main__":
    run_server()