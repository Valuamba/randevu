import asyncio
import websockets
import logging
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)


class Server:
    clients = set()
    
    async def register(self, websocket: WebSocketServerProtocol) -> None:
        self.clients.add(websocket)
        logging.info(f'{websocket.remote_address} connects.')
        
    async def unregister(self, websocket: WebSocketServerProtocol) -> None:
        self.clients.remove(websocket)
        logging.info(f'{websocket.remote_address} disconnects.')
        
    async def send_to_clients(self, message: str) -> None:
        if self.clients:
            await asyncio.wait([asyncio.create_task(client.send('biba')) for client in self.clients])
        
    async def distribute(self, websocket: WebSocketServerProtocol) -> None:
        async for message in websocket:
            await self.send_to_clients(message)
        
    async def ws_handler(self, websocket: WebSocketServerProtocol) -> None:
        await self.register(websocket)
        for i in range(100):
            await websocket.send('Big mak')
            await asyncio.sleep(2)
        # try:
        #     await self.distribute(websocket)
        # finally:
        #     await self.unregister(websocket)
    
    
# server = Server()
# start_server = websockets.serve(server.ws_handler, 'localhost', 6748)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(start_server)
# loop.run_forever()

#!/usr/bin/env python

import asyncio
import websockets
import logging
import time
# logger = logging.getLogger('websockets')
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler())

async def echo(websocket):
    # for i in range(100):
    #     await websocket.send('Kek')
    #     resp = await websocket.recv()
    #     await asyncio.sleep(1)
    #     pass
    start = time.time()
    logging.info(f'Websocket {websocket.remote_address} connected')
    try:
        async for message in websocket:
            await websocket.send(message + ' 1205')
    finally:
        end = time.time()
        logging.info(f'Elapsed {end - start}')

async def main():
    async with websockets.serve(echo, "localhost", 6748, timeout=10):
        await asyncio.Future()  # run forever

asyncio.run(main())