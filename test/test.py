import unittest as ut
from unittest.mock import patch

from src.player import Player, PlayerType
from src.game import Game

import unittest.mock

# def mock_input(message):
#   print("called")
#   return 5

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
    pass

  def test_get_amount_from_user(self):
    """
      get_amount_from_user
      1. gets int amount from user
      2. validates that the input is non-negative
    """
    pass

  def test_calc_round_cost(self):
    """
      calc_round_cost
      1. calc holding and underage costs
      2. update round cost
    """
    pass

  def test_log(self):
    """
      log
      1. returns a df of all round stats
    """
    pass


if __name__ == "__main__":
  ut.main()



