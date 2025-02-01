import asyncio
from server import RedisServer


async def main():
    server = RedisServer(host="localhost", port=6379)
    server_task = asyncio.create_task(server.start())

    # Give the server a few seconds to start
    await asyncio.sleep(2)

    print("Testing with a simple client...")
    reader, writer = await asyncio.open_connection("localhost", 6379)

    # Send a simple command to the server (e.g., a SET command)
    command = "SET key1 value1\r\n"
    print(f"Sending: {command}")
    writer.write(command.encode())
    await writer.drain()

    # Wait for the server response
    response = await reader.read(100)
    print(f"Received: {response.decode()}")

    # Send a GET command to retrieve the key
    command = "GET key1\r\n"
    print(f"Sending: {command}")
    writer.write(command.encode())
    await writer.drain()

    # Wait for the server response
    response = await reader.read(100)
    print(f"Received: {response.decode()}")

    # Delay the server shutdown a little to ensure communication is completed
    print("Delaying server shutdown...")
    await asyncio.sleep(2)

    # Trigger server shutdown
    print("Triggering server shutdown...")
    server.initiate_shutdown()

    # Wait for the server to shutdown
    await server_task

    print("Server has shut down.")

if __name__ == "__main__":
    asyncio.run(main())