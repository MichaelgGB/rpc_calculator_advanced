# client_stubs.py
import json
import socket

class RPCError(Exception):
    """Custom exception for errors returned by the RPC server."""
    pass

class TCPClientStub:
    """A client stub that communicates over a persistent TCP connection."""
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def _remote_call(self, method_name, params):
        # 1. Construct the JSON request.
        request = json.dumps({"method": method_name, "params": params})
        
        # 2. Send the request.
        self.sock.sendall(request.encode('utf-8'))
        
        # 3. Receive the response.
        response_json = self.sock.recv(1024).decode('utf-8')
        response = json.loads(response_json)
        
        # 4. Handle success or error.
        if response.get("error"):
            raise RPCError(response["error"])
        return response.get("result")

    # The public methods that the user calls.
    def add(self, x, y): return self._remote_call('add', [x, y])
    def subtract(self, x, y): return self._remote_call('subtract', [x, y])
    def multiply(self, x, y): return self._remote_call('multiply', [x, y])
    def divide(self, x, y): return self._remote_call('divide', [x, y])
    
    def close(self):
        self.sock.close()


class UDPClientStub:
    """A client stub that communicates over connectionless UDP."""
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (host, port)
        self.sock.settimeout(5.0) # Set a timeout for responses.

    def _remote_call(self, method_name, params):
        request = json.dumps({"method": method_name, "params": params})
        self.sock.sendto(request.encode('utf-8'), self.server_addr)
        
        try:
            response_json, _ = self.sock.recvfrom(1024)
            response = json.loads(response_json.decode('utf-8'))
            
            if response.get("error"):
                raise RPCError(response["error"])
            return response.get("result")
        except socket.timeout:
            raise RPCError("Request timed out. Server did not respond.")

    # The public methods that the user calls.
    def add(self, x, y): return self._remote_call('add', [x, y])
    def subtract(self, x, y): return self._remote_call('subtract', [x, y])
    def multiply(self, x, y): return self._remote_call('multiply', [x, y])
    def divide(self, x, y): return self._remote_call('divide', [x, y])
    
    def close(self):
        self.sock.close()