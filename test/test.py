import unittest as ut
from src.player import Player, PlayerType
from src.game import Game

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

  def test_send_outbound(self):
    """
      test outbound
      1. gets input from user
      2. checks if the input is available
      3. Updates end_inv, start_inv, and shipped
      4. Updates downstream received
    """
    upstream = Player(PlayerType.DISTRIBUTOR, 15, 5, 10)
    upstream.shipped = [5]
    player = Player(PlayerType.RETAILER, 15, 5, 10)

    t_lead_time = 1

    player.receive_inbound(upstream, t_lead_time)
    self.assertEqual(player.received, [0, 0])
    self.assertEqual(player.start_inv, [15, 20])

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

  def test_calc_round_cost(self):
    """
      calc_round_cost
      1. calc holding and underage costs
      2. update round cost
    """


if __name__ == "__main__":
  ut.main()



