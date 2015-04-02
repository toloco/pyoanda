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
    def setUp(self):
        pass

    def tearDown(self):
        pass

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

    def test_order_creation(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True) as mock_method:
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
        with mock.patch.object(Client, '_Client__call', return_value=True) as mock_method:
            assert c.create_order("GPB_EUR", 1)





