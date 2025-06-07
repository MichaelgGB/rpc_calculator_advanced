import json

class Calculator:
    """The actual calculator implementation."""
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

    def multiply(self, x, y):
        return x * y

    def divide(self, x, y):
        if y == 0:
            # This error will be caught and formatted into a JSON response.
            raise ValueError("Cannot divide by zero.")
        return x / y

# A single instance of our calculator that the dispatcher will use.
_calculator_instance = Calculator()

def handle_rpc_request(json_request: str) -> str:
    """
    Parses a JSON-RPC request, calls the appropriate method, and returns a JSON-RPC response.
    This is the core dispatcher for the server.
    """
    try:
        request = json.loads(json_request)
        method_name = request.get("method")
        params = request.get("params", [])

        # Get the actual method from our calculator instance.
        method_to_call = getattr(_calculator_instance, method_name)
        
        # Call the method with the provided parameters.
        result = method_to_call(*params)
        
        # Format a success response.
        response = {"result": result, "error": None}

    except Exception as e:
        # If anything goes wrong, format an error response.
        response = {"result": None, "error": str(e)}

    return json.dumps(response)