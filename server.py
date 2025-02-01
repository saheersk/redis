import asyncio
import signal
from datastore import DataStore
from handler import ClientHandler


class RedisServer:
    def __init__(self, host="localhost", port=6379):
        self.host = host
        self.port = port
        self.server = None
        self._shutdown_event = asyncio.Event()
        self.data_store = DataStore()

    async def start(self):
        loop = asyncio.get_event_loop()

        # Start the server
        self.server = await loop.create_server(self.client_connected, self.host, self.port)
        addr = self.server.sockets[0].getsockname()
        print(f"Serving on {addr}")

        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, self.initiate_shutdown)

        await self._shutdown_event.wait()
        await self.shutdown()

    async def client_connected(self, reader, writer):
        handler = ClientHandler(reader, writer, self.data_store)
        await handler.handle()

    def initiate_shutdown(self):
        """Initiate shutdown by setting the shutdown event."""
        self._shutdown_event.set()

    async def shutdown(self):
        print("Shutting down server...")
        if self.server:
            self.data_store.save_data()
            self.server.close()
            await self.server.wait_closed()
            print("Server shut down.")
        else:
            print("Server was not running.")