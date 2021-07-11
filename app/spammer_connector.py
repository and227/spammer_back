import asyncio
from os import name, write
from core.config import settings
from fastapi.encoders import jsonable_encoder

from typing import Tuple
from collections import namedtuple
import json


SpammerConnector = namedtuple('SpammerConnector', ('reader', 'writer'))


async def open_spammer_connection():
    reader, writer = await asyncio.open_connection(settings.SPAMMER_SERVER, int(settings.SPAMMER_PORT))
    connector = SpammerConnector(reader=reader, writer=writer)
    return connector


async def close_spammer_connection(connector):
    connector.writer.close()
    await connector.writer.wait_closed()


async def connect_spammer():
    reader, writer = await asyncio.open_connection(settings.SPAMMER_SERVER, int(settings.SPAMMER_PORT))
    connector = SpammerConnector(reader=reader, writer=writer)
    yield connector
    connector.writer.close()
    await connector.writer.wait_closed()


async def send_spammer_command(connector, command):
    connector.writer.write(json.dumps(jsonable_encoder(command)).encode())
    print(json.dumps(jsonable_encoder(command)).encode())
    await connector.writer.drain()
    answer = await connector.reader.read(8192)
    return json.loads(answer.decode())['data']