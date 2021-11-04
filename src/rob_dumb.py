#!/usr/bin/env python

import asyncio
import websockets

class RobDumb:
    def __init__(self, socket):
        self.socket = socket

    async def do_something(self):
        await self.socket.send("Rob dumb something")

async def rob_dumb():
    async with websockets.connect('ws://localhost:8765') as websocket:
      try:
          rd = RobDumb(websocket)
          await rd.do_something()
      except Exception as e:
          print(e)

asyncio.get_event_loop().run_until_complete(rob_dumb())