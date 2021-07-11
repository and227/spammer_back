from os import write
from threading import Thread, Event
import asyncio
from asyncio import CancelledError
import websockets
import json
import random
from typing import Dict
import logging

FORMAT = '|%(levelname)s| %(asctime)s: %(filename)s %(funcName)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


class ListenThread(Thread):
    def __init__(self, group=None, target=None, name=None, daemon=False, *args, **kwargs):
        super().__init__(group=group, target=target, name=name,
                         args=args, kwargs=kwargs, daemon=daemon)
        self.args = args
        self.kworgs = kwargs
        self.spammers_info = kwargs.get('spammers_info', None)
        self.restart_event = kwargs.get('restart_event', None)

    async def add_spammers(self, data):
        added_ids = []
        if isinstance(data, list):
            for item in data:
                self.spammers_info[item['id']] = item
                added_ids.append(item['id'])
        else:
            self.spammers_info[data['id']] = data
            added_ids.append(data['id'])
        return added_ids

    async def delete_spammers(self, ids):
        deleted_ids = []
        if len(ids) == 0:
            for id in self.spammers_info:
                deleted_ids.append(id)
        else:
            for id in ids:
                if id in self.spammers_info:
                    deleted_ids.append(id)

        for id in deleted_ids:
            del self.spammers_info[id]

        return deleted_ids

    async def start_spammers(self, ids):
        started_ids = []
        if len(ids) == 0:
            for id in self.spammers_info:
                self.spammers_info[id]['state'] = 'working'
                started_ids.append(id)
        else:
            for id in ids:
                if id in self.spammers_info:
                    self.spammers_info[id]['state'] = 'working'
                    started_ids.append(id)
        return started_ids

    async def stop_spammers(self, ids):
        stopped_ids = []
        if len(ids) == 0:
            for id in self.spammers_info:
                self.spammers_info[id]['state'] = 'stopped'
                stopped_ids.append(id)
        else:
            for id in ids:
                if id in self.spammers_info:
                    self.spammers_info[id]['state'] = 'stopped'
                    stopped_ids.append(id)
        return stopped_ids


    async def get_spammers_state(self, id_list):
        spammers_state_list = []
        for id in id_list:
            if id in self.spammers_info:
                spammers_state_list.append(spammers_info[id])
        return spammers_state_list

    async def handle_command(self, reader, writer):
        data: bytes = await reader.read(8192)
        if data:
            print(data)
            message = json.loads(data.decode('utf-8'))
            print(message)
            command = message['command']

            if command == 'state':
                spammers_state_list = await self.get_spammers_state(message['data'])
                writer.write(json.dumps({'command': 'state', 'data': spammers_state_list}).encode('utf-8'))
                await writer.drain()
            elif command == 'add':
                self.restart_event.set()
                add_spammers_ids = await self.add_spammers(message['data'])
                message['data'] = add_spammers_ids
                writer.write(json.dumps(message).encode('utf-8'))
                await writer.drain()
                logger.info(f'Spammers with ids {add_spammers_ids} added')
            elif command == 'start':
                self.restart_event.set()
                start_spammers_ids = await self.start_spammers(message['data'])
                message['data'] = start_spammers_ids
                writer.write(json.dumps(message).encode('utf-8'))
                await writer.drain()
                logger.info(f'Spammers with ids {start_spammers_ids} started')
            elif command == 'stop':
                self.restart_event.set()
                stop_spammers_ids = await self.stop_spammers(message['data'])
                message['data'] = stop_spammers_ids
                writer.write(json.dumps(message).encode('utf-8'))
                await writer.drain()
                logger.info(f'Spammers with ids {stop_spammers_ids} stopped')
            elif command == 'delete':
                self.restart_event.set()
                deleted_spammers_ids = await self.delete_spammers(message['data'])
                message['data'] = deleted_spammers_ids
                writer.write(json.dumps(message).encode('utf-8'))
                await writer.drain()
                logger.info(f'Spammers with ids {deleted_spammers_ids} deleted')
            elif command == 'replace':
                self.restart_event.set()
                await self.delete_spammers([])
                add_spammers_ids = await self.add_spammers(message['data'])
                message['data'] = add_spammers_ids
                writer.write(json.dumps(message).encode('utf-8'))
                await writer.drain()
                logger.info(f'Spammers with ids {add_spammers_ids} replace old')
            else:
                logger.info(f'Unknown command "{command}"')
        else:
            logger.info('Socket connection closed')

    async def websocket_handle_command(self, websocket, path):
        data: str = await websocket.recv()
        message = json.loads(data)
        command = message['command']
        if command == 'state':
            spammers_state_list = await self.get_spammers_state(message['data'])
            await websocket.send(json.dumps(spammers_state_list))

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        server = asyncio.start_server(
            client_connected_cb=self.handle_command,
            host='0.0.0.0',
            port=9000,
            loop=loop
        )
        websocket_server = websockets.serve(
            self.websocket_handle_command, '0.0.0.0', 9001)

        server_future = loop.run_until_complete(server)
        websocket_server_future = loop.run_until_complete(websocket_server)

        logger.info('Serving on {}'.format(
            server_future.sockets[0].getsockname()))
        logger.info('Websocket serving on {}'.format(
            websocket_server_future.sockets[0].getsockname()))

        try:
            loop.run_forever()
        except KeyboardInterrupt as e:
            # close all servers and event loop
            server_future.close()
            loop.run_until_complete(server_future.wait_closed())
            websocket_server_future.close()
            loop.run_until_complete(websocket_server_future.wait_closed())
            loop.close()


async def spammer(data):
    while True:
        await asyncio.sleep(random.randint(5, 30))
        if data['state'] == 'working':
            data['target']['current'] += 1
            if data['target']['current'] >= 100:
                data['target']['total'] += 1
            current_id = data["id"]
            current_val = data["target"]["current"]
            total_val = data["target"]["total"]
            logger.info(
                f'spammer with id {current_id} make {current_val} current and {total_val} total')


class SpammerThread(Thread):
    def __init__(self, group=None, target=None, 
        name=None, daemon=False, *args, **kwargs):
        super().__init__(group=group, target=target, name=name,
                         args=args, kwargs=kwargs, daemon=daemon)
        self.args = args
        self.kworgs = kwargs
        self.spammers_info = kwargs.get('spammers_info', None)
        self.restart_event = kwargs.get('restart_event', None)

    async def event_waiter(self, cancel_group):
        # wait for stop event, if set, cansel group of spammers and
        # stop waiting to reach new cycle of while loop
        while True:
            if self.restart_event.is_set():
                cancel_group.cancel()
                await asyncio.sleep(3)
                self.restart_event.clear()
                break
            else:
                await asyncio.sleep(1)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        while True:
            spammers_group = asyncio.gather(
                *(spammer(spammer_info) for spammer_info in self.spammers_info.values())
            )
            run_group = asyncio.gather(
                spammers_group, self.event_waiter(spammers_group))
            
            try:
                loop.run_until_complete(run_group)
            except CancelledError as e:
                pass


if __name__ == '__main__':
    spammers_info: Dict[int, Dict] = {}
    restart_event = Event()

    listen_thread = ListenThread(
        spammers_info=spammers_info,
        restart_event=restart_event,
    )
    spammers_thread = SpammerThread(
        spammers_info=spammers_info,
        restart_event=restart_event,
    )

    listen_thread.start()
    spammers_thread.start()
