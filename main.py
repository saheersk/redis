import asyncio


class RedisServer:
    def __init__(self, host="localhost", port=6379):
        self.host = host
        self.port = port
        self.server = None

    async def start(self):
        print("Starting Redis server...")


if __name__ == "__main__":
    asyncio.run(RedisServer().start())