import websockets
import asyncio

# server details
PORT = 5001
print("server is listening on port" + str(PORT))


async def echo(websocket, path):
    print("a client just connected")
    async for message in websocket:
        print("message received from client:" + message)
        await websocket.send("Pong: " + message)

start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
# to make sure the server doesn't stop working
asyncio.get_event_loop().run_forever()
