try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pyoanda.exceptions import BadRequest

from .integration_test_case import IntegrationTestCase


class TestTradeAPI(IntegrationTestCase):
    def test_get_trades(self):
        assert self.client.get_trades()

    def test_get_trade(self):
        order = self.build_order(immediate=True)
        result = self.client.create_order(order)
        assert self.client.get_trade(result['tradeOpened']['id'])
        assert self.client.get_trade(trade_id=result['tradeOpened']['id'])

    def test_update_trade(self):
        order = self.client.create_order(self.build_order(immediate=True))
        trade = self.client.get_trade(order['tradeOpened']['id'])

        for stop_loss in [round(trade['price'] * 0.5, 5), 0]:
            result = self.client.update_trade(trade['id'], stop_loss=stop_loss)
            self.assertEqual(stop_loss, result['stopLoss'])

        for take_profit in [round(trade['price'] * 1.5, 5), 0]:
            result = self.client.update_trade(
                trade['id'],
                take_profit=take_profit
            )
            self.assertEqual(take_profit, result['takeProfit'])

        for trailing_stop in [100, 0]:
            result = self.client.update_trade(
                trade['id'],
                trailing_stop=trailing_stop
            )
            self.assertEqual(trailing_stop, result['trailingStop'])

    @unittest.skip("Failing due to Oanda bug, HTTP 500 on close")
    def test_close_trade(self):
        order = self.client.create_order(self.build_order(immediate=True))
        trade = self.client.get_trade(order['tradeOpened']['id'])
        assert self.client.close_trade(trade['id'])

        with self.assertRaises(BadRequest):
            # Cannot close twice
            self.client.close_trade(trade['id'])

        with self.assertRaises(BadRequest):
            # No longer in trades once closed
            self.client.get_trade(trade['id'])
