from abc import ABC, abstractmethod
from datastore import DataStore


class BaseCommand(ABC):
    @abstractmethod
    async def execute(self, *args) -> str:
        pass


class SetCommand(BaseCommand):
    async def execute(self, key: str, value: str) -> str:
        DataStore()._data[key] = value
        return "+OK\r\n"


class GetCommand(BaseCommand):
    async def execute(self, key: str) -> str:
        value = DataStore()._data.get(key)
        return f"${len(value)}\r\n{value}\r\n" if value else "$-1\r\n"


class DelCommand(BaseCommand):
    async def execute(self, key: str) -> str:
        return ":1\r\n" if DataStore()._data.pop(key, None) else ":0\r\n"
