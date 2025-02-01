import pytest
import asyncio
from unittest import mock

from commands import SetCommand, GetCommand, DelCommand
from handler import CommandHandler
from server import RedisServer, DataStore


@pytest.fixture
def mock_data_store():
    with mock.patch.object(DataStore, 'load_data') as mock_load_data, \
         mock.patch.object(DataStore, 'save_data') as mock_save_data:
        mock_load_data.return_value = None
        mock_save_data.return_value = None
        yield DataStore()


@pytest.mark.asyncio
async def test_set_command(mock_data_store):
    set_command = SetCommand()
    response = await set_command.execute("key1", "value1")
    assert response == "+OK\r\n"
    assert mock_data_store._data.get("key1") == "value1"


@pytest.mark.asyncio
async def test_get_command(mock_data_store):
    mock_data_store._data["key1"] = "value1"
    get_command = GetCommand()
    response = await get_command.execute("key1")
    assert response == "$6\r\nvalue1\r\n"

    # Testing for non-existent key
    response = await get_command.execute("nonexistent")
    assert response == "$-1\r\n"


@pytest.mark.asyncio
async def test_del_command(mock_data_store):
    mock_data_store._data["key1"] = "value1"
    del_command = DelCommand()
    response = await del_command.execute("key1")
    assert response == ":1\r\n"
    assert "key1" not in mock_data_store._data

    # Trying to delete non-existent key
    response = await del_command.execute("nonexistent")
    assert response == ":0\r\n"


@pytest.mark.asyncio
async def test_command_handler(mock_data_store):
    command_handler = CommandHandler()

    # Testing SET command
    response = await command_handler.execute_command("SET", "key1", "value1")
    assert response == "+OK\r\n"
    assert mock_data_store._data.get("key1") == "value1"

    response = await command_handler.execute_command("SET", "key2", "value2")
    assert response == "+OK\r\n"
    assert mock_data_store._data.get("key2") == "value2"

    response = await command_handler.execute_command("SET", "key3", "value3")
    assert response == "+OK\r\n"
    assert mock_data_store._data.get("key3") == "value3"

    # Testing GET command
    response = await command_handler.execute_command("GET", "key1")
    assert response == "$6\r\nvalue1\r\n"

    # Testing DEL command
    response = await command_handler.execute_command("DEL", "key1")
    assert response == ":1\r\n"
    assert "key1" not in mock_data_store._data

    # Testing unknown command
    response = await command_handler.execute_command("UNKNOWN")
    assert response == "-ERR Unknown command\r\n"


@pytest.mark.asyncio
async def test_redis_server_shutdown():
    with mock.patch.object(DataStore, 'save_data') as mock_save_data:
        server = RedisServer(host="localhost", port=6379)

        server_task = asyncio.create_task(server.start())

        await asyncio.sleep(0.1)

        server.initiate_shutdown()

        await server_task

        mock_save_data.assert_called_once()
