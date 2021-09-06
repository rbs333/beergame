from src.game import Game
from src.player import Player, PlayerType

def main():
  num_rounds = 10
  transport_lead_time = 1
  order_lead_time = 1
  starting_inv = 15
  starting_demand = 5

  g = Game(num_rounds, transport_lead_time, order_lead_time)
  g.initialize_players(starting_inv, starting_demand)
  g.run()


if __name__ == "__main__":
  main()
