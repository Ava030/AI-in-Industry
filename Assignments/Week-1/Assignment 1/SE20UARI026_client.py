import websockets
import asyncio

async def listen():
    #since both server and client are on the same system, you can use localhost or the local IP address (127.0.0.1)
    url  = "ws://127.0.0.1:5001"

    async with websockets.connect(url) as websocket:
        while True:
            message = input("Type a message to send to server: ")
            await websocket.send(message)
            print(f"Sent message to server: {message}")

            msg = await websocket.recv()
            print(f"Received message from server: {msg}")

asyncio.get_event_loop().run_until_complete(listen())
