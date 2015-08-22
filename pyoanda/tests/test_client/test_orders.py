try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    from unittest import mock
except ImportError:
    import mock
from requests.exceptions import RequestException

from pyoanda.client import Client
from pyoanda.order import Order


class TestOrdersAPI(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            self.client = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    def test_credentials_pass(self):
        with mock.patch.object(
            Client, '_Client__call',
            return_value={"message": "good one"}
        ):
            assert self.client.get_credentials()

    def test_credentials_fail(self):
        with mock.patch.object(Client, '_Client__call', return_value=()):
            assert not self.client.get_credentials()

        e = RequestException("I fail")
        with mock.patch.object(Client, '_Client__call', side_effect=e):
            assert not self.client.get_credentials()

    def test_get_orders(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_orders()

    def test_get_order(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_order(1)

    def test_create_order(self):
        order = Order(instrument="GBP_EUR", units=1, side="buy", type="market")
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.create_order(order)

    def test_update_order(self):
        order = Order(instrument="GBP_EUR", units=1, side="buy", type="market")
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.update_order(1, order)

    def test_close_order(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.close_order(1)
