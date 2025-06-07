# tcp_concurrent/server_tcp_concurrent_async_rpc.py
import asyncio
from main_programs.rpc_logic import handle_rpc_request

HOST = '127.0.0.1'
PORT = 8000

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    addr = writer.get_extra_info('peername')
    print(f"[Async] New connection from {addr}")

    try:
        # This is the essential loop for handling multiple requests from one client.
        while True:
            data = await reader.read(1024)
            if not data:
                print(f"[Async] Client {addr} disconnected.")
                break
            
            response_json = handle_rpc_request(data.decode('utf-8'))
            writer.write(response_json.encode('utf-8'))
            await writer.drain()
            
    except ConnectionResetError:
        print(f"[Async] Client {addr} forcefully closed the connection.")
    except Exception as e:
        print(f"[Async] An unexpected error occurred with {addr}: {e}")
    finally:
        print(f"[Async] Closing connection from {addr}")
        if not writer.is_closing():
            writer.close()
            await writer.wait_closed()

async def main():
    server = await asyncio.start_server(handle_client, HOST, PORT)
    addr = server.sockets[0].getsockname()
    print(f"Async TCP RPC Server serving on {addr}. Press Ctrl+C to shut down.")

    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutdown signal received. Server is closing.")