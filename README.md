# RPC Calculator in Python

This project is a hands-on demonstration of various network programming models. It implements a simple Remote Procedure Call (RPC) calculator from scratch to compare different server architectures.

The core goal is to show how the same application can be served using:
- **Iterative vs. Concurrent** designs.
- **Connection-Oriented (TCP) vs. Connectionless (UDP)** protocols.
- **Threading, Multiprocessing, and `asyncio`** for concurrency.

## Project Structure

- `main_programs/`: Contains the core logic, including the menu-driven client.
- `tcp_iterative/` & `udp_iterative/`: Simple servers that handle one request at a time.
- `tcp_concurrent/` & `udp_concurrent/`: Advanced servers that handle multiple clients/requests simultaneously.

## How to Run

You need **two separate terminal windows** and Python 3.8+ installed.

### Step 1: Start a Server

In your first terminal, navigate to the project's root directory and choose a server to run. Use the `python -m` command to run it as a module.

**Example: Start the Threaded Concurrent TCP Server**
```bash
# Make sure you are in the rpc_calculator/ directory
python python -m iterative_tcp.server

#In the second terminal fire up the client.py
python main_programs/main_client.py
