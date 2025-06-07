# udp_concurrent/server_udp_concurrent_async_rpc.py
import asyncio
from main_programs.rpc_logic import handle_rpc_request

HOST = '127.0.0.1'
PORT = 8000

class CalculatorUdpProtocol(asyncio.DatagramProtocol):
    """An asyncio Protocol class to handle UDP datagram events."""
    
    def connection_made(self, transport: asyncio.DatagramTransport):
        """Called when the UDP endpoint is ready."""
        self.transport = transport

    def datagram_received(self, data: bytes, addr):
        """Called by the event loop for each received datagram."""
        print(f"[Async] Received datagram from {addr}")
        response_json = handle_rpc_request(data.decode('utf-8'))
        self.transport.sendto(response_json.encode('utf-8'), addr)

    def error_received(self, exc):
        print(f"An error occurred in the UDP endpoint: {exc}")

async def main():
    """Main coroutine to start and run the UDP server."""
    loop = asyncio.get_running_loop()
    
    print(f"Async UDP RPC Server serving on {HOST}:{PORT}")
    print("Press Ctrl+C to shut down.")
    
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: CalculatorUdpProtocol(),
        local_addr=(HOST, PORT)
    )
    
    # The try/finally block ensures the transport is closed on exit
    try:
        # This will run forever until cancelled by Ctrl+C
        await asyncio.Future()
    finally:
        transport.close()

if __name__ == "__main__":
    # The try/except KeyboardInterrupt here provides the clean exit message
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown signal received. Server is closing gracefully.")