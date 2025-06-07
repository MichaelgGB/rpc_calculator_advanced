# udp_iterative/server_udp_iterative_rpc.py
import socket
import sys

from main_programs.rpc_logic import handle_rpc_request

HOST = '127.0.0.1'
PORT = 8000

def run_server():
    """Runs the iterative UDP server with a graceful shutdown."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((HOST, PORT))
        print(f"Iterative UDP RPC Server listening on {HOST}:{PORT}")
        print("Press Ctrl+C to shut down.")

        # --- START OF FIX: Add try...except block ---
        try:
            while True: # Main loop to wait for datagrams
                # This call blocks until a datagram is received
                data, addr = s.recvfrom(1024)
                
                print(f"Received request from {addr}")
                response_json = handle_rpc_request(data.decode('utf-8'))
                
                s.sendto(response_json.encode('utf-8'), addr)
        
        except KeyboardInterrupt:
            print("\nShutdown signal received. Server is closing.")
        # --- END OF FIX ---

if __name__ == "__main__":
    run_server()