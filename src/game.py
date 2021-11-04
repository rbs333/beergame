import pandas as pd
from src.player import PlayerType, Player

class Game:
  """ overall game class """
  def __init__(self, num_rounds: int, order_lead_time: int, transport_lead_time: int, simulate: bool):
    print("init")
    self.players = []
    self.num_rounds = num_rounds
    self.order_lead_time = order_lead_time
    self.transport_lead_time = transport_lead_time
    self.simulate = simulate

  def initialize_players(self, starting_inv, starting_demand, player_clients):
    retailer = Player(PlayerType.RETAILER, starting_inv, starting_demand, 
                      self.num_rounds, simulate=self.simulate, websocket=player_clients["RETAILER"])
    supplier = Player(PlayerType.SUPPLIER, starting_inv, starting_demand, 
                      self.num_rounds, simulate=self.simulate, websocket=player_clients["SUPPLIER"])
    distributor = Player(PlayerType.DISTRIBUTOR, starting_inv, starting_demand, 
                      self.num_rounds, simulate=self.simulate, websocket=player_clients["DISTRIBUTOR"])
    manufacturer = Player(PlayerType.MANUFACTURER, starting_inv, starting_demand, 
                          self.num_rounds, simulate=self.simulate, websocket=player_clients["MANUFACTURER"])

    self.players = [retailer, supplier, distributor, manufacturer]
  
  def take_turn(self, player, upstream, downstream, current_round):
    print("executing turn \n")
    player.current_round = current_round
    player.receive_inbound(upstream, self.transport_lead_time)
    player.send_outbound(downstream, self.transport_lead_time)
    player.order(upstream, self.order_lead_time)
    player.calculate_round_cost()

    print("\n player log: \n", player.log())

  def save_logs(self):
    cols = list(self.players[0].log().columns)
    cols.append("player")
    all_players = pd.DataFrame(columns=cols)

    for p in self.players:
      log = p.log()
      log = log[log["round"] != self.num_rounds + 1]
      log["player"] = str(p.player_type).split(".")[1]
      all_players = all_players.append(log)
      
    cost_view = all_players.pivot(index="round", columns="player", values="demand")
    ax = cost_view.plot(figsize=(10,5), alpha=0.6)
    ax.set_title("Demand curve")
    ax.set_xlabel("week")
    ax.set_ylabel("demand")
    ax.text(1, all_players.demand.max() / 2, "Note: retailer demand is the actual demand.")

    fig = ax.get_figure()
    fig.savefig("src/game_logs/demand_chart.png")
    all_players.to_csv("src/game_logs/game_logs.csv")

  def run(self):
    print("Started game")
    print(f"Rounds: {self.num_rounds} \n\n")
    current_round = 0
    while current_round < self.num_rounds:
      print(f"Starting round: {current_round + 1} \n")
      # Take each players turn
      for i, player in enumerate(self.players):
        print(f"Round {current_round + 1} | Player {player.player_type}")
        upstream = self.players[i+1] if i < len(self.players) - 1 else None
        downstream = self.players[i-1] if i > 0 else None
        self.take_turn(player, upstream, downstream, current_round)

      current_round += 1

    self.save_logs()
    
