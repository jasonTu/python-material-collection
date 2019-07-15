import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    counter = 0
    while True:
        greeting += str(counter)
        await websocket.send(greeting)
        print(f"> {greeting}")
        counter += 1
        await asyncio.sleep(1)

start_server = websockets.serve(hello, "0.0.0.0", 8080)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
