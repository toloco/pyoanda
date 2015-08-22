import json
import requests_mock

try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    from unittest import mock
except ImportError:
    import mock
from zipfile import ZipFile
from io import BytesIO

from pyoanda.client import Client


class TestTransactionAPI(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            self.client = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    def test_get_transactions(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_transactions()

    def test_get_transaction(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_transaction(1)

    @requests_mock.Mocker()
    def test_request_transaction_history(self, m):
        location = 'http://example.com/transactions.json.gz'
        m.get(
            requests_mock.ANY,
            headers={'Location': location}, status_code=202
        )
        self.assertEqual(location, self.client.request_transaction_history())

    @requests_mock.Mocker()
    def test_get_transaction_history(self, m):
        # Mock zip file content
        content = BytesIO()
        with ZipFile(content, 'w') as zip:
            zip.writestr('transactions.json', json.dumps({'ok': True}))
        content.seek(0)

        # Mock requests, one HEAD to check if it's there, one GET once it is
        location = 'http://example.com/transactions.json.gz'
        m.head(location, status_code=200)
        m.get(location, body=content, status_code=200)

        method = 'request_transaction_history'
        with mock.patch.object(Client, method, return_value=location):
            transactions = self.client.get_transaction_history()
            assert transactions['ok']
            assert m.call_count == 2

    @requests_mock.Mocker()
    def test_get_transaction_history_slow(self, m):
        """Ensures that get_transaction_history retries requests."""
        # Mock zip file content
        content = BytesIO()
        with ZipFile(content, 'w') as zip:
            zip.writestr('transactions.json', json.dumps({'ok': True}))
        content.seek(0)

        # Mock requests, one HEAD to check if it's there, one GET once it is
        location = 'http://example.com/transactions.json.gz'
        m.head(location, [{'status_code': 404}, {'status_code': 200}])
        m.get(location, body=content, status_code=200)

        method = 'request_transaction_history'
        with mock.patch.object(Client, method, return_value=location):
            transactions = self.client.get_transaction_history()
            assert transactions['ok']
            assert m.call_count == 3

    @requests_mock.Mocker()
    def test_get_transaction_history_gives_up(self, m):
        """Ensures that get_transaction_history eventually gives up."""
        # Mock requests, one HEAD to check if it's there, one GET once it is
        location = 'http://example.com/transactions.json.gz'
        m.head(location, [{'status_code': 404}, {'status_code': 404}])

        method = 'request_transaction_history'
        with mock.patch.object(Client, method, return_value=location):
            transactions = self.client.get_transaction_history(.3)
            assert not transactions
            # Possible timing issue, may be one or the other
            assert m.call_count == 2 or m.call_count == 3

    @requests_mock.Mocker()
    def test_get_transaction_history_handles_bad_files(self, m):
        """Ensures that get_transaction_history gracefully handles bad files.
        """
        # Mock requests, one HEAD to check if it's there, one GET once it is
        location = 'http://example.com/transactions.json.gz'
        m.head(location, status_code=200)
        m.get(location, text='invalid', status_code=200)

        method = 'request_transaction_history'
        with mock.patch.object(Client, method, return_value=location):
            transactions = self.client.get_transaction_history()
            assert not transactions
