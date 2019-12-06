import asyncio
import websockets


'''
async def client(number):
    base_uri = 'ws://10.206.67.81:80/ws/{}'.format(number)
    async with websockets.connect(base_uri) as websocket:
        while True:
            data = await websocket.recv()
            print('{}: {}'.format(number, data))

asyncio.get_event_loop().run_until_complete(client(1))
'''

'''
async def main():
    clients = [client(item) for item in range(100)]
    await asyncio.gather(*clients)


asyncio.run(main())
'''

import asyncio
import websockets

async def hello():
    number = 1
    base_uri = 'ws://10.206.67.81:80/ws/{}'.format(number)
    async with websockets.connect(base_uri) as websocket:
        # await asyncio.sleep(5)
        while True:
            data = await websocket.recv()
            print('{}: {}'.format(number, data))

asyncio.get_event_loop().run_until_complete(hello())
