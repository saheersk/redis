import asyncio
from server import RedisServer


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    server = RedisServer()
    loop.run_until_complete(server.start())
