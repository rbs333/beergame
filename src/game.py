from src.player import PlayerType, Player

class Game:
  """ overall game class """
  def __init__(self, num_rounds: int, order_lead_time: int, transport_lead_time: int):
    print("init")
    self.players = []
    self.num_rounds = num_rounds
    self.order_lead_time = order_lead_time
    self.transport_lead_time = transport_lead_time

  def initialize_players(self, starting_inv, starting_demand):
    retailer = Player(PlayerType.RETAILER, starting_inv, starting_demand, self.num_rounds)
    suplier = Player(PlayerType.SUPPLIER, starting_inv, starting_demand, self.num_rounds)
    distributor = Player(PlayerType.DISTRIBUTOR, starting_inv, starting_demand, self.num_rounds)
    manufacturer = Player(PlayerType.MANUFACTURER, starting_inv, starting_demand, self.num_rounds)
    self.players = [retailer, suplier, distributor, manufacturer]
  
  def take_turn(self, player, upstream, downstream, current_round):
    print("executing turn \n")
    player.current_round = current_round
    player.receive_inbound(upstream, self.transport_lead_time)
    player.send_outbound(downstream, self.transport_lead_time)
    player.order(upstream, self.order_lead_time)

    print("\n player log: \n", player.log())

  def run(self):
    print("Started game")
    print(f"Rounds: {self.num_rounds} \n\n")
    current_round = 0
    while current_round <= self.num_rounds:
      print(f"Starting round: {current_round + 1} \n")
      # Take each players turn
      for i, player in enumerate(self.players):
        print(f"Round {current_round + 1} | Player {player.player_type}")
        upstream = self.players[i+1] if i < len(self.players) - 1 else None
        downstream = self.players[i-1] if i > 0 else None
        self.take_turn(player, upstream, downstream, current_round)

      current_round += 1