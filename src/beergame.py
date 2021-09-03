from enum import Enum, auto
import numpy as np
import pandas as pd

class PlayerType(Enum):
  MANUFACTURER = auto()
  DISTRIBUTOR = auto()
  SUPPLIER = auto()
  RETAILER = auto()

class Game:
  """ overall game class """
  def __init__(self, players: list, num_rounds: int):
    self.players = players
    self.num_rounds = num_rounds
  
  def run(self):
    current_round = 1
    while current_round < self.num_rounds:
      # Take each players turn
      for i, player in enumerate(self.players):
        upstream = self.players[i+1] if i < len(self.players) - 1 else None
        downstream = self.players[i-1] if i > 0 else None
        take_turn(player, upstream, downstream)

      current_round += 1


class Player:
  """ player class """
  def __init__(self, player_type, starting_inv, starting_demand):
    self.player_type = player_type
    self.demand = [starting_demand]
    self.received = [0]
    self.shipped = [0]
    self.on_hand = [starting_inv]
    self.total_inventory = []
    self.round_cost = []
    self.current_round = 0

  def receive_inbound(self, upstream):
    if upstream is None:
      print("Manuf level")
      return

    # product received - updates total inventory
    self.received.append(upstream.shipped[-1])
    self.total_inventory.append(self.received[-1] + self.on_hand[-1])

  def send_outbound(self, downstream):
    if downstream is None:
      print("downstream is customer")
      return

    round_demand = self.demand[self.current_round]

    # send all units available to meet demand
    amount_shipped = min(round_demand, self.total_inventory[self.current_round])

    if amount_shipped < round_demand:
      # incur cost of underage
      self.round_cost.append(round_demand - amount_shipped)

    # update downstream received
    downstream.received.append(amount_shipped)

    # set on hand for next round
    self.on_hand.append(self.total_inventory[self.current_round] - amount_shipped)

  def order(self, upstream):
    if upstream is None:
      print("Manuf level")
      return
    # do validation on input that amount is okay
    desired_amount = self.get_amount_from_user()
    upstream.demand.append(desired_amount)

  def get_amount_from_user(self):
    # eventually and input method
    print(f"Demand is {self.demand[-1]} you have {self.total_inventory[-1]} units available")
    print("Enter order amount: ")
    order_amount = input()
    return order_amount
    
def take_turn(player: Player, upstream, downstream):
  player.receive_inbound(upstream)
  player.send_outbound(downstream)
  player.order(upstream)


def main():
  starting_inv = 15
  starting_demand = 5

  players = [ Player(pt, starting_inv, starting_demand) for pt in PlayerType]

  game = Game(players, 10)

  game.run()


if __name__ == "__main__":
  main()
