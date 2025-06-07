# tcp_concurrent/server_tcp_concurrent_threads_rpc.py
import socket
import threading
from main_programs.rpc_logic import handle_rpc_request

HOST = '127.0.0.1'
PORT = 8000

def client_handler(conn: socket.socket, addr):
    """Handles a single client connection in its own thread."""
    print(f"[Thread for {addr}] started.")
    with conn:
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"[Thread for {addr}] Client disconnected.")
                    break
                response_json = handle_rpc_request(data.decode('utf-8'))
                conn.sendall(response_json.encode('utf-8'))
        except ConnectionResetError:
             print(f"[Thread for {addr}] Client connection reset.")
        except Exception as e:
            print(f"[Thread for {addr}] An error occurred: {e}")
    print(f"[Thread for {addr}] finished.")

def run_server():
    """Main server function with robust flag-based shutdown."""
    
    # --- START OF FIX: Use a shutdown flag ---
    shutdown_flag = threading.Event()
    active_threads = []
    # --- END OF FIX ---
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(1.0) 
        print(f"Concurrent TCP RPC Server (Threads) listening on {HOST}:{PORT}.")
        print("Press Ctrl+C to shut down.")

        # --- START OF FIX: Main loop checks the flag ---
        while not shutdown_flag.is_set():
            try:
                conn, addr = s.accept()
                thread = threading.Thread(target=client_handler, args=(conn, addr))
                thread.daemon = True
                thread.start()
                active_threads.append(thread)
                active_threads = [t for t in active_threads if t.is_alive()]
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                print("\nShutdown signal received...")
                shutdown_flag.set()
        # --- END OF FIX ---

        print("Waiting for active client threads to finish (max 5 seconds)...")
        for thread in active_threads:
            thread.join(timeout=5.0)
            
        print("Server has shut down gracefully.")

if __name__ == "__main__":
    run_server()