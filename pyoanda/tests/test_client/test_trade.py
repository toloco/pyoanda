try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from pyoanda.client import Client


class TestTradeAPI(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            self.client = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    def test_get_trades(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_trades()

    def test_get_trade(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_trade(1)
            assert self.client.get_trade(trade_id=1)

    def test_update_trade(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.update_trade(1)
            assert self.client.update_trade(1, 0)
            assert self.client.update_trade(1, 1)
            assert self.client.update_trade(1, None, 0)
            assert self.client.update_trade(1, None, 1)
            assert self.client.update_trade(1, None, None, 0)
            assert self.client.update_trade(1, None, None, 1)

    def test_close_trade(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.close_trade(1)
            assert self.client.close_trade(trade_id=1)
