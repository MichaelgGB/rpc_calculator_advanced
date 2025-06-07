# tcp_concurrent/server_tcp_concurrent_processes_rpc.py
import socket
import multiprocessing
from main_programs.rpc_logic import handle_rpc_request

HOST = '127.0.0.1'
PORT = 8000

def client_handler(conn: socket.socket, addr):
    """Handles a single client connection in its own process."""
    process_name = multiprocessing.current_process().name
    print(f"[{process_name} for {addr}] started.")
    with conn:
        try:
            # --- START OF FIX: Add a loop inside the handler ---
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"[{process_name} for {addr}] Client disconnected gracefully.")
                    break # Exit the loop if the client closes the connection
                
                response_json = handle_rpc_request(data.decode('utf-8'))
                conn.sendall(response_json.encode('utf-8'))
            # --- END OF FIX ---
        except ConnectionResetError:
             print(f"[{process_name} for {addr}] Client connection was reset.")
        except Exception as e:
            print(f"[{process_name} for {addr}] An error occurred: {e}")

    print(f"[{process_name} for {addr}] finished.")

def run_server():
    """Main server function to accept connections and spawn processes."""
    active_processes = []
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        s.settimeout(1.0)
        print(f"Concurrent TCP RPC Server (Processes) listening on {HOST}:{PORT}.")
        print("Press Ctrl+C to shut down.")

        try:
            while True:
                try:
                    conn, addr = s.accept()
                    process = multiprocessing.Process(target=client_handler, args=(conn, addr))
                    process.start()
                    active_processes.append(process)
                    conn.close() # Parent must close its copy
                    active_processes = [p for p in active_processes if p.is_alive()]
                except socket.timeout:
                    continue
        except KeyboardInterrupt:
            print("\nShutdown signal received. Stopping new connections.")
        finally:
            print("Waiting for active client processes to finish...")
            for process in active_processes:
                process.join()
            print("All processes finished. Server is shut down.")

if __name__ == "__main__":
    run_server()