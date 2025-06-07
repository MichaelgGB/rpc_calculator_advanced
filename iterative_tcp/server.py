# tcp_iterative/server_tcp_iterative_rpc.py
import socket
import sys

# Make sure to adjust this path if your structure is different
# This allows importing from a sibling directory like 'main_programs'
# when running as a module from the root.
from main_programs.rpc_logic import handle_rpc_request

HOST = '127.0.0.1'
PORT = 8000

def run_server():
    """Runs the iterative TCP server with a graceful shutdown."""
    # The 'with' statement ensures the socket is always closed on exit
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # This option allows the server to restart quickly
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Iterative TCP RPC Server listening on {HOST}:{PORT}")
        print("Press Ctrl+C to shut down.")

        # --- START OF FIX: Add try...except block ---
        try:
            while True: # Main loop to accept new clients
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True: # Loop to handle requests from the connected client
                        data = conn.recv(1024)
                        if not data:
                            break # Client disconnected
                        
                        response_json = handle_rpc_request(data.decode('utf-8'))
                        conn.sendall(response_json.encode('utf-8'))
                    
                    print(f"Connection with {addr} closed.")
        
        except KeyboardInterrupt:
            print("\nShutdown signal received. Server is closing.")
        # --- END OF FIX ---

if __name__ == "__main__":
    run_server()