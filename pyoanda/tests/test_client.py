try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from ..client import Client
from ..exceptions import BadCredentials


class TestClient(unittest.TestCase):
    def test_connect_pass(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True) as mock_method:
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
    def test_connect_fail(self):
        with mock.patch.object(Client, 'get_credentials', return_value=False) as mock_method:
            with self.assertRaises(BadCredentials):
                c = Client(
                    ("http://mydomain.com", "http://mystreamingdomain.com"),
                    "my_account",
                    "my_token"
                )

class TestOrders(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True) as mock_method:
            self.client = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    def test_order_creation(self):
        with mock.patch.object(Client, '_Client__call', return_value=True) as mock_method:
            assert self.client.create_order("GPB_EUR", 1)

    def test_get_orders(self):
        with mock.patch.object(Client, '_Client__call', return_value=True) as mock_method:
            assert self.client.get_orders()

    def test_get_order(self):
        pass

    def test_create_order(self):
        pass

    def test_update_order(self):
        pass

    def test_close_order(self):
        pass

