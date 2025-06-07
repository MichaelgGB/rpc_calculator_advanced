import socket
from client_stubs import TCPClientStub, UDPClientStub, RPCError

# --- Configuration ---
HOST = '127.0.0.1'
PORT = 8000

# --- Menu Definitions ---

# A data structure to define all available servers
SERVERS = [
    # --- TCP Servers ---
    {"id": 1, "desc": "Iterative_TCP", "proto": "tcp"},
    {"id": 2, "desc": "Concurrent_TCP_Threads", "proto": "tcp"},
    {"id": 3, "desc": "Concurrent_TCP_Processes", "proto": "tcp"},
    {"id": 4, "desc": "Concurrent_TCP_AsyncI/O", "proto": "tcp"},
    # --- UDP Servers ---
    {"id": 5, "desc": "Iterative_UDP", "proto": "udp"},
    {"id": 6, "desc": "Concurrent_UDP_Threads", "proto": "udp"},
    {"id": 7, "desc": "Concurrent_UDP_Processes", "proto": "udp"},
    {"id": 8, "desc": "Concurrent_UDP_AsyncI/O", "proto": "udp"},
]

# A data structure for the calculator operations
OPERATIONS = [
    {"id": 1, "desc": "Add", "method": "add"},
    {"id": 2, "desc": "Subtract", "method": "subtract"},
    {"id": 3, "desc": "Multiply", "method": "multiply"},
    {"id": 4, "desc": "Divide", "method": "divide"},
]

# --- Main Functions ---

def select_server():
    """Displays a menu for the user to select which server to connect to."""
    print("--- Select a Server to Test ---")
    for server in SERVERS:
        print(f"{server['id']}. {server['desc']}")
    print("0. Exit")
    
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice == 0:
                return None # Signal to exit
            
            for server in SERVERS:
                if server['id'] == choice:
                    print(f"\nAttempting to connect to: {server['desc']}")
                    return server # Return the chosen server's dictionary
            
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def run_calculator_ui(client_stub):
    """
    Displays the main calculator UI and handles user operations
    after a successful connection has been made.
    """
    print("\n--- RPC Calculator ---")
    while True:
        print("\n--- Select an Operation ---")
        for op in OPERATIONS:
            print(f"{op['id']}. {op['desc']}")
        print("0. Exit to Main Menu")
        
        try:
            # 1. Get user's choice of operation
            op_choice = int(input("Enter operation number: "))
            
            if op_choice == 0:
                break # Exit the calculator loop
            
            # 2. Find the chosen operation from our list
            chosen_op = next((op for op in OPERATIONS if op['id'] == op_choice), None)

            if not chosen_op:
                print("Invalid operation number. Please try again.")
                continue

            # 3. Get numbers from the user
            num1 = int(input(f"  Enter first number for {chosen_op['desc']}: "))
            num2 = int(input(f"  Enter second number for {chosen_op['desc']}: "))
            
            # 4. Dynamically call the correct method on the client stub
            method_to_call = getattr(client_stub, chosen_op['method'])
            result = method_to_call(num1, num2)
            
            print(f"  ✅ SUCCESS: Result from server is {result}")

        except ValueError:
            print("  ❌ ERROR: Invalid input. Please enter integers for numbers and choices.")
        except RPCError as e:
            # Catches custom errors sent back from the server (e.g., divide by zero)
            print(f"  ❌ SERVER ERROR: {e}")
        except Exception as e:
            # Catches unexpected client-side errors (e.g., connection drops)
            print(f"  ❌ An unexpected error occurred: {e}")
            break # Exit the loop on critical errors

def main():
    """Main application entry point."""
    while True:
        chosen_server = select_server()
        
        if not chosen_server:
            print("Exiting application. Goodbye!")
            break # Exit the main loop if user chose 0

        client_stub = None
        try:
            # Create the correct stub based on the user's choice
            if chosen_server['proto'] == 'tcp':
                client_stub = TCPClientStub(HOST, PORT)
            else: # 'udp'
                client_stub = UDPClientStub(HOST, PORT)
            
            # Run the main calculator interface
            run_calculator_ui(client_stub)

        except ConnectionRefusedError:
            print(f"\n❌ CONNECTION FAILED: Could not connect to the server at {HOST}:{PORT}.")
            print("Please make sure you have started the correct server script first.\n")
        except Exception as e:
            print(f"A critical error occurred: {e}")
        finally:
            # Ensure the connection is always closed gracefully
            if client_stub and hasattr(client_stub, 'close'):
                client_stub.close()
            print("\nConnection closed. Returning to server selection menu.")

if __name__ == "__main__":
    main()