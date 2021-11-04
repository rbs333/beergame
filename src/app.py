#!/usr/bin/env python

import asyncio
import websockets

async def echo(websocket, path):
    print(websocket)
    async for message in websocket:
        print("message from client: ", message)
        await websocket.send(f"Robert's server touched this: {message}")

async def get_order(websocket, path):
    await websocket.send("Your turn")


asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8765))

asyncio.get_event_loop().run_forever()