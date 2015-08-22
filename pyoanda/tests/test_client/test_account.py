try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    from unittest import mock
except ImportError:
    import mock

from pyoanda.client import Client


class TestAccountAPI(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            self.client = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    def test_create_account(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.create_account()

    def test_create_account_with_currency(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.create_account('AUD')
            assert self.client.create_account(currency='AUD')

    def test_get_accounts(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_accounts()

    def test_get_accounts_with_username(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_accounts('bob')
            assert self.client.get_accounts(username='bob')
