#!/usr/bin/env python

# WS server example that synchronizes state across clients

import asyncio
import json
import logging
import websockets

from src.game import Game

logging.basicConfig()

STATE = {"value": 0, "active": "RETAILER"}

PLAYER_KEY = ["Retailer", "Supplier", "Distributor", "Manufacturer"]
PLAYERS = list()
CONNECTIONS = set()

def run_game(users):
  num_rounds = 20
  transport_lead_time = 1
  order_lead_time = 1
  starting_inv = 10
  starting_demand = 5
  simulate = True

  # pass users to game for 
  g = Game(num_rounds, transport_lead_time, order_lead_time, simulate)
  g.initialize_players(starting_inv, starting_demand, PLAYERS)
  g.run()

# def state_event():
#   return json.dumps({"type": "state", **STATE})

def users_event():
  return json.dumps({"type": "users", "count": len(PLAYERS)})

def add_player():
  return json.dumps({"type": "assign_role", "role": PLAYERS[-1]["name"]})

def order_event():
  return json.dumps({"type": "state", **STATE})


async def game_server(websocket, path):
  try:
    # Register user
    if len(PLAYERS) < 4:
      user = {
        PLAYER_KEY[len(PLAYERS)]: websocket
      }

      PLAYERS.append(user)
      CONNECTIONS.add(websocket)
      # update all clients on the overall count
      websockets.broadcast(CONNECTIONS, users_event())

      # send specific message to client which player they are
      await websocket.send(json.dumps({
        "type": "assign_role",
        "role": PLAYER_KEY[len(PLAYERS)-1]
      }))
    elif len(PLAYERS) == 4:
      # start the game
      run_game(PLAYERS)
  
    else:
      print("no more players for this game!")
    # Send current state to user
    # await websocket.send(state_event())
    # Manage state changes
    async for message in websocket:
      data = json.loads(message)
      print("from client data: ", data)
  finally:
      # Unregister user
      CONNECTIONS.remove(websocket)
      websockets.broadcast(CONNECTIONS, users_event())


async def main():
  async with websockets.serve(game_server, "localhost", 6789):
    await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())