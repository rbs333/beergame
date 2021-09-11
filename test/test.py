import unittest as ut
from unittest.mock import patch

from src.player import Player, PlayerType
from src.game import Game

import unittest.mock

class TestPlayerMethods(ut.TestCase):
  def test_receive_inbound(self):
    num_rounds = 2
    upstream = Player(PlayerType.DISTRIBUTOR, 15, 5, num_rounds)
    upstream.shipped = [5, 0]

    player = Player(PlayerType.RETAILER, 15, 5, num_rounds)
    player.current_round = 1

    t_lead_time = 1

    player.receive_inbound(upstream, t_lead_time)
    self.assertEqual(player.received, [0, 5])

  # @patch('src.player.Player.get_amount_from_user', return_value=5)
  def test_send_outbound(self):
    """
      test outbound
      1. gets input from user
      2. checks if the input amount is available
      3. Updates end_inv, start_inv, and shipped
      4. Updates downstream received
    """
    num_rounds = 2
    starting_inv = 15
    starting_demand = 5
    t_lead_time = 1

    with ut.mock.patch('src.player.Player.get_amount_from_user') as mock_input:
      player = Player(PlayerType.SUPPLIER, starting_inv, starting_demand, num_rounds)
      downstream = Player(PlayerType.RETAILER, starting_inv, starting_demand, num_rounds)

      mock_input.return_value = 5
      player.send_outbound(downstream, t_lead_time)

      self.assertEqual(player.end_inv, [10, 0])
      self.assertEqual(player.start_inv, [15, 10])
      self.assertEqual(player.shipped, [5, 0])

  def test_order(self):
    """
      order method
      1. gets input from user
      2. sets upstream demand
    """
    num_rounds = 2
    starting_inv = 15
    starting_demand = 5
    o_lead_time = 1

    with ut.mock.patch('src.player.Player.get_amount_from_user') as mock_input:
      upstream = Player(PlayerType.SUPPLIER, starting_inv, starting_demand, num_rounds)
      player = Player(PlayerType.RETAILER, starting_inv, starting_demand, num_rounds)

      mock_input.return_value = 5
      player.order(upstream, o_lead_time)

      self.assertEqual(upstream.demand, [5, 5])

  def test_calc_round_cost(self):
    """
      calc_round_cost
      1. calc holding and underage costs
      2. update round cost
    """
    num_rounds = 2
    starting_inv = 15
    starting_demand = 5
    player = Player(PlayerType.DISTRIBUTOR, starting_inv, starting_demand, num_rounds)
    player.demand = [5, 5]
    player.shipped = [4, 5]
    player.end_inv = [11, 6]
    player.start_inv = [15, 11]

    unit_holding_cost = 1
    unit_underage_cost = 1

    # rnd_cost = max(demand - shipped, 0) + units_held
    # 1st rnd_cost = 1*(5 - 4) + 1*(15) = 16
    # 2nd rnd_cost = 1*(5 - 5) + 1*(11) = 11
    player.calculate_round_cost(unit_holding_cost, unit_underage_cost)
    player.current_round += 1
    player.calculate_round_cost(unit_holding_cost, unit_underage_cost)

    self.assertEqual(player.round_cost, [16, 11])

  def test_log(self):
    """
      log
      1. returns a df of all round stats
    """
    num_rounds = 2
    starting_inv = 15
    starting_demand = 5
    player = Player(PlayerType.DISTRIBUTOR, starting_inv, starting_demand, num_rounds)
    
    log_df = player.log()
    expected_cols = ["round", "start_inv", "received", "demand", "shipped", "end_inv", "round_cost"]

    self.assertEqual(list(log_df.columns), expected_cols)
    self.assertEqual(log_df.shape, (2, 7))

  def test_simulate_demand(self):
    """
      simulates demand via normal distribution
      1. consider avg_demand and std_demand passed to function
      2. returns positive value
    """
    num_rounds = 2
    player = Player(PlayerType.RETAILER, 15, 5, num_rounds)

    d = player.simulate_demand()
    avg = sum(d) / len(d)
    self.assertEqual(len(d), 2)
    self.assertGreater(avg, player.LB)
    self.assertLess(avg, player.UB)

  def test_simulate_order(self):
    """
      simulates order
      1. calculates avg order
      2. makes order for average
    """
    num_rounds = 2
    player = Player(PlayerType.RETAILER, 15, 5, num_rounds)

    o = player.simulate_order()
    self.assertGreater(o, 0)

  def test_manf_production(self):
    """
      simulates order
      1. calculates avg order
      2. makes order for average
    """

  def test_retailer_demand(self):
    """
      simulates order
      1. calculates avg order
      2. makes order for average
    """



if __name__ == "__main__":
  ut.main()



