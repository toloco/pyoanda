try:
    import unittest2 as unittest
except ImportError:
    import unittest

import json
from decimal import Decimal

from .. import SANDBOX
from ..client import Client
from ..order import Order
from ..exceptions import BadCredentials, BadRequest
from pprint import pprint
from datetime import datetime, timedelta

client = Client(SANDBOX)
user = client.create_account(currency="GBP")
client.account_id = user['accountId']

class IntegrationTestCase(unittest.TestCase):
    def build_order(self, immediate=False):
        """ Build an order to be used with create_order.

            Building an order is commonly required in the integration
            tests, so this makes it easy.

            Parameters
            ----------
            immediate: bool
                Whether to place an order that will be met immediately
                or not; this is achieved by examining current prices and
                bidding well below for non-immediate or by placing a
                market order for immediate.

            Returns an Order
        """
        if immediate:
            return Order(instrument="GBP_USD", units=1, side="buy",
                        type="market")

        expiry = datetime.utcnow() + timedelta(minutes=1)
        prices = self.client.get_prices("GBP_USD", False)
        price = prices['prices'][0]
        at = round(price['bid'] * 0.9, 5)

        # order must not be met straight away, otherwise we can't get it back
        return Order(instrument="GBP_USD", units=1, side="buy",
                type="limit", price=at, expiry=expiry.isoformat())

    def setUp(self):
        self.client = client

class TestAccountAPI(IntegrationTestCase):
    def test_create_account(self):
        assert self.client.create_account()

    def test_create_account_with_currency(self):
        assert self.client.create_account('GBP')
        assert self.client.create_account(currency='GBP')

    def test_get_accounts(self):
        assert self.client.get_accounts(username=user['username'])


class TestClientFoundation(IntegrationTestCase):
    def test_connect_pass(self):
        assert self.client.get_credentials()

    def test_connect_fail(self):
        with self.assertRaises(BadRequest):
            client = Client(SANDBOX, 999999999)


class TestOrderAPI(IntegrationTestCase):
    def test_get_orders(self):
        assert self.client.get_orders()

    def test_get_order(self):
        order = self.build_order()
        result = self.client.create_order(order)
        assert self.client.get_order(result['orderOpened']['id'])
        assert self.client.get_order(order_id=result['orderOpened']['id'])

    def test_create_order(self):
        order = self.build_order()
        assert self.client.create_order(order)

    def test_update_order(self):
        order = self.build_order()
        result = self.client.create_order(order)
        assert self.client.update_order(result['orderOpened']['id'], order)

    def test_close_order(self):
        order = self.build_order()
        result = self.client.create_order(order)
        assert self.client.close_order(result['orderOpened']['id'])

        with self.assertRaises(BadRequest):
            # Cannot close twice
            self.client.close_order(result['orderOpened']['id'])

        with self.assertRaises(BadRequest):
            # No longer in orders once closed
            self.client.get_order(result['orderOpened']['id'])

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
            self.assertEquals(stop_loss, result['stopLoss'])

        for take_profit in [round(trade['price'] * 1.5, 5), 0]:
            result = self.client.update_trade(trade['id'],
                    take_profit=take_profit)
            self.assertEquals(take_profit, result['takeProfit'])

        for trailing_stop in [100, 0]:
            result = self.client.update_trade(trade['id'],
                    trailing_stop=trailing_stop)
            self.assertEquals(trailing_stop, result['trailingStop'])

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

class TestInstrumentsAPI(IntegrationTestCase):
    def test_get_instruments_pass(self):
        assert self.client.get_instruments()

    def test_get_prices_unstreamed(self):
        assert self.client.get_prices(instruments="EUR_GBP", stream=False)

    def test_get_prices_streamed(self):
        resp = self.client.get_prices(instruments="EUR_GBP", stream=True)
        prices = resp.iter_lines();
        assert next(prices)

    def test_get_instrument_history(self):
        assert self.client.get_instrument_history('EUR_GBP')


class TestPositionAPI(IntegrationTestCase):
    def test_get_positions(self):
        self.client.get_positions()

    def test_get_position(self):
        order = self.build_order(immediate=True)
        result = self.client.create_order(order)
        assert self.client.get_position('GBP_USD')
        assert self.client.get_position(instrument='GBP_USD')

    @unittest.skip("Failing due to Oanda bug, HTTP 500 on close")
    def test_close_position(self):
        order = self.build_order(immediate=True)
        result = self.client.create_order(order)
        assert self.client.close_position('GBP_USD')

        # cannot close twice
        with self.assertRaises(BadRequest):
            assert self.client.close_position('GBP_USD')

        # cannot get position if closed
        with self.assertRaises(BadRequest):
            assert self.client.get_position('GBP_USD')

class TestTransactionAPI(IntegrationTestCase):
    def test_get_transactions(self):
        assert self.client.get_transactions()

    def test_get_transaction(self):
        order = self.build_order(immediate=True)
        result = self.client.create_order(order)
        transactions = self.client.get_transactions()
        transaction = transactions['transactions'][0]
        assert self.client.get_transaction(transaction['id'])

    def test_request_transaction_history(self):
        assert self.client.request_transaction_history()
