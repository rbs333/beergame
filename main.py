from src.game import Game
from src.player import Player, PlayerType

def main():
  num_rounds = 20
  transport_lead_time = 1
  order_lead_time = 1
  starting_inv = 10
  starting_demand = 5
  simulate = True

  g = Game(num_rounds, transport_lead_time, order_lead_time, simulate)
  g.initialize_players(starting_inv, starting_demand)
  g.run()


if __name__ == "__main__":
  main()
