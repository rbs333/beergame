from enum import Enum, auto
from dataclasses import dataclass

import numpy as np
import pandas as pd
import json

class PlayerType(Enum):
  MANUFACTURER = auto()
  DISTRIBUTOR = auto()
  SUPPLIER = auto()
  RETAILER = auto()

@dataclass
class Player:
  """ player class """
  def __init__(self, player_type, starting_inv, starting_demand, num_rounds, simulate=False, websocket=None, avg_demand=5, LB=0, UB=10):
    self.player_type = player_type
    self.num_rounds = num_rounds
    self.current_round = 0
    self.simulate = simulate
    self.avg_demand = avg_demand
    self.starting_demand = starting_demand
    self.LB = LB
    self.UB = UB
    self.websocket = websocket

    # todo figure out a cleaner way of doing the indexing
    # self.index = num_rounds + 1
    # demand will get updated programatically
    self.demand = [starting_demand] * (self.num_rounds)
    self.received = [0] * (self.num_rounds)
    self.shipped = [0] * (self.num_rounds)
    self.back_orders = [0] * (self.num_rounds)
    self.start_inv = [0] * (self.num_rounds)
    self.end_inv = [0] * (self.num_rounds)
    self.round_cost = [0] * (self.num_rounds)
    self.orders = [0] * (self.num_rounds)

    # set initial conditions
    self.start_inv[0] = starting_inv
    self.end_inv[0] = max(starting_inv - self.shipped[0] + self.received[0], 0)

    if self.player_type == PlayerType.RETAILER:
      print("initializing demand for whole game")
      self.demand = self.simulate_demand_naive()

  def log(self) -> pd.DataFrame:
    return pd.DataFrame({
      "round": [i+1 for i in range(self.num_rounds)],
      "start_inv": self.start_inv,
      "received": self.received,
      "demand": self.demand,
      "shipped": self.shipped,
      "back_orders": self.back_orders,
      "end_inv": self.end_inv,
      "round_cost": self.round_cost,
      "ordered": self.orders
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
    current_demand = self.demand[self.current_round] + self.back_orders[self.current_round]

    available_units = self.received[self.current_round] + self.start_inv[self.current_round]
    message = f"Demand is {current_demand} you have {available_units} available units. \nHow many would you like to ship?"
    # send all units available to meet demand

    default_amount_shipped = min(current_demand, available_units)

    if not self.simulate:
      amount_shipped = self.get_amount_from_user(message)
      print("\n input: ", amount_shipped)

      if amount_shipped > available_units:
        print("Can't ship that many shipping default")
        amount_shipped = default_amount_shipped
    else:
      amount_shipped = default_amount_shipped

    if amount_shipped < current_demand:
      index = self.current_round + 1
      if index >= self.num_rounds:
        return

      self.back_orders[index] = current_demand - amount_shipped

    self.end_inv[self.current_round] = self.start_inv[self.current_round] \
                                        + self.received[self.current_round] \
                                          - amount_shipped

    self.start_inv[self.current_round + 1] = self.end_inv[self.current_round]

    self.shipped[self.current_round] = amount_shipped

    if downstream is None:
      print("downstream is customer")
      return

    # update downstream received
    index = self.current_round + 1 + transport_lead_time

    if index >= self.num_rounds:
      return
    
    downstream.received[index] = amount_shipped

  def order(self, upstream, order_lead_time) -> None:
    available_units = self.end_inv[self.current_round]
    message = f"You have {available_units}. \nHow many units would you like to order? \n"

    # do validation on input that amount is okay
    if not self.simulate and self.websocket:
      desired_amount = self.ping_client(available_units)
    elif not self.simulate:
      desired_amount = self.get_amount_from_user(message)
    else:
      desired_amount = self.simulate_order()

    if upstream is None:
      print(f"Manuf produces {desired_amount} units")
      self.orders[self.current_round] = desired_amount

      index = self.current_round + order_lead_time

      if index >= self.num_rounds:
        return
      
      self.received[self.current_round + order_lead_time] = desired_amount
      return

    self.orders[self.current_round] = desired_amount

    index = self.current_round + order_lead_time + 1
    if index >= self.num_rounds:
      return

    upstream.demand[index] = desired_amount

  def ping_client_order(self, available_units) -> int:
    round_info = {
      "type": "get_order",
      "round": self.current_round,
      "available_units": available_units,
      "player": self.player_type
    }
    
    def dump_round_info():
      json.dumps(round_info) 

    self.websocket.send(round_info, dump_round_info())
  
  def dump_client_info(self):
    return 

  def get_amount_from_user(self, message) -> int:
    print(message)
    print("Enter amount: ")
    order_amount = int(input())

    if order_amount < 0:
      print("stop trying to break the game dingus")
      raise ValueError

    return order_amount

  def simulate_demand_triangular(self) -> int:
    demand = np.random.triangular(self.LB, self.avg_demand, self.UB, self.num_rounds)
    return [round(d) for d in demand]

  def simulate_demand_naive(self) -> int:
    # could maybe make simulate into its own class to increase cohesion
    before_demand_increased = int(self.num_rounds / 3)
    print(before_demand_increased)
    demand_start = [self.starting_demand] * before_demand_increased
    print(demand_start)
    demand_end = [self.starting_demand*2] * (self.num_rounds - before_demand_increased)

    demand = demand_start + demand_end
    return demand
  
  def simulate_order(self) -> int:
    # stats = self.log()
    # order = round(stats['demand'][stats['demand'] != 0].mean())
    order = round(self.demand[max(self.current_round-1, 0)] + self.back_orders[self.current_round])
    return order

  def calculate_round_cost(self, unit_holding_cost=1, unit_underage_cost=1) -> None:
    holding_cost = unit_holding_cost * self.start_inv[self.current_round]
    underage_cost = unit_underage_cost * max(self.demand[self.current_round] - self.shipped[self.current_round], 0)
    self.round_cost[self.current_round] = holding_cost + underage_cost