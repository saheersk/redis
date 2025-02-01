from commands import SetCommand, GetCommand, DelCommand


class CommandHandler:
    def __init__(self):
        self.commands = {
            "SET": SetCommand(),
            "GET": GetCommand(),
            "DEL": DelCommand(),
        }

    async def execute_command(self, command: str, *args) -> str:
        command_instance = self.commands.get(command.upper())
        if command_instance:
            return await command_instance.execute(*args)
        return "-ERR Unknown command\r\n"


class ClientHandler:
    def __init__(self, reader, writer, data_store):
        self.reader = reader
        self.writer = writer
        self.command_handler = CommandHandler()

    async def handle(self):
        while True:
            try:
                data = await self.reader.read(100)
                if not data:
                    break
                message = data.decode("utf-8").strip()
                print(f"Request: {message}")
                command_parts = message.split()
                response = await self.command_handler.execute_command(*command_parts)
                self.writer.write(response.encode("utf-8"))
                await self.writer.drain()
            except Exception as e:
                print(f"Error: {e}")
                break

        self.writer.close()
        await self.writer.wait_closed()
