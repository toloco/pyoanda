try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from ..client import Client
from ..order import Order
from ..exceptions import BadCredentials


class TestClient(unittest.TestCase):
    def test_connect_pass(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    def test_connect_fail(self):
        with mock.patch.object(Client, 'get_credentials', return_value=False):
            with self.assertRaises(BadCredentials):
                Client(
                    ("http://mydomain.com", "http://mystreamingdomain.com"),
                    "my_account",
                    "my_token"
                )


class TestOrders(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            self.client = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    def test_order_creation(self):
        order = Order()
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.create_order(order)

    def test_get_orders(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_orders()

    def test_get_order(self):
        pass

    def test_create_order(self):
        pass

    def test_update_order(self):
        pass

    def test_close_order(self):
        pass
