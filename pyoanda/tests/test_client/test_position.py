try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from pyoanda.client import Client


class TestPositionAPI(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            self.client = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    def test_get_positions(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_positions()

    def test_get_position(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_position('AUD_USD')
            assert self.client.get_position(instrument='AUD_USD')

    def test_close_position(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.close_position('AUD_USD')
            assert self.client.close_position(instrument='AUD_USD')
