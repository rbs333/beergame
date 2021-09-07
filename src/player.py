from enum import Enum, auto
from dataclasses import dataclass

import numpy as np
import pandas as pd

class PlayerType(Enum):
  MANUFACTURER = auto()
  DISTRIBUTOR = auto()
  SUPPLIER = auto()
  RETAILER = auto()

@dataclass
class Player:
  """ player class """
  def __init__(self, player_type, starting_inv, starting_demand, num_rounds, simulate=False, avg_demand=5, std_demand=1):
    self.player_type = player_type
    self.num_rounds = num_rounds
    self.current_round = 0
    self.simulate = simulate
    self.avg_demand = avg_demand
    self.std_demand = std_demand

    self.demand = [0] * (num_rounds)
    self.received = [0] * (num_rounds)
    self.shipped = [0] * (num_rounds)
    self.start_inv = [0] * (num_rounds)
    self.end_inv = [0] * (num_rounds)
    self.round_cost = [0] * (num_rounds)

    # set initial conditions
    self.start_inv[0] = starting_inv
    self.end_inv[0] = max(starting_inv - self.shipped[0] + self.received[0], 0)
    self.demand[0] = starting_demand

  def log(self) -> pd.DataFrame:
    return pd.DataFrame({
      "round": [i+1 for i in range(self.num_rounds)],
      "start_inv": self.start_inv,
      "received": self.received,
      "demand": self.demand,
      "shipped": self.shipped,
      "end_inv": self.end_inv,
      "round_cost": self.round_cost
      })

  def receive_inbound(self, upstream, transport_lead_time) -> None:
    if upstream is None:
      print("Manuf level")
      return

    # look at what the upstream provider shipped x lead time ago
    ship_status = self.current_round - transport_lead_time

    if ship_status < 0:
      self.received[self.current_round] = 0
      return

    inbound = upstream.shipped[ship_status]
    self.received[self.current_round] = inbound

  def send_outbound(self, downstream, transport_lead_time) -> None:
    current_demand = self.demand[self.current_round]

    available_units = self.received[self.current_round] + self.start_inv[self.current_round]
    message = f"Demand is {current_demand} you have {available_units} available units. \nHow many would you like to ship?"
    # send all units available to meet demand

    if not self.simulate:
      amount_shipped = self.get_amount_from_user(message)
    else:
      amount_shipped = self.simulate_demand()

    print("\n input: ", amount_shipped)

    if amount_shipped < available_units:
      print("You can't ship that many. Sending min(demand, available)")
      amount_shipped = min(current_demand, available_units)

    self.end_inv[self.current_round] = self.start_inv[self.current_round] \
                                        + self.received[self.current_round] \
                                          - amount_shipped

    self.start_inv[self.current_round + 1] = self.end_inv[self.current_round]

    self.shipped[self.current_round] = amount_shipped

    if downstream is None:
      print("downstream is customer")
      return

    # update downstream received
    downstream.received[self.current_round + transport_lead_time] = amount_shipped

  def order(self, upstream, order_lead_time) -> None:
    if upstream is None:
      print("Manuf level")
      return

    available_units = self.end_inv[self.current_round]
    message = f"You have {available_units}. \nHow many units would you like to order? \n"

    # do validation on input that amount is okay
    if not self.simulate:
      desired_amount = self.get_amount_from_user(message)
    else:
      desired_amount = self.simulate_order()

    upstream.demand[self.current_round + order_lead_time] = desired_amount

  def get_amount_from_user(self, message) -> int:
    print(message)
    print("Enter amount: ")
    order_amount = int(input())

    if order_amount < 0:
      print("stop trying to break the game dingus")
      raise ValueError

    return order_amount

  def simulate_demand(self) -> int:
    demand = int(np.random.normal(self.avg_demand, self.std_demand))
    return demand

  def simulate_order(self) -> int:
    stats = self.log()
    avg_demand = int(stats['demand'][stats['demand' != 0]].mean())
    return avg_demand

  def calculate_round_cost(self, unit_holding_cost, unit_underage_cost) -> None:
    holding_cost = unit_holding_cost * self.start_inv[self.current_round]
    underage_cost = unit_underage_cost * min(self.demand[self.current_round] - self.shipped[self.current_round], 0)
    self.round_cost[self.current_round] = holding_cost + underage_cost