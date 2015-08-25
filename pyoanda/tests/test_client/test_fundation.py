import json
import requests
import requests_mock

try:
    import unittest2 as unittest
except ImportError:
    import unittest
try:
    from unittest import mock
except ImportError:
    import mock
from decimal import Decimal

from pyoanda.client import Client
from pyoanda.exceptions import BadCredentials, BadRequest


class TestClientFundation(unittest.TestCase):
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

    @requests_mock.Mocker()
    def test_call_pass(self, m):
        """Ensure that successful HTTP response codes pass."""
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
            c.session = requests.Session()

        for status_code in [200, 201, 202, 301, 302]:
            m.get(requests_mock.ANY, text='{}', status_code=status_code)
            c._Client__call(
                uri="http://example.com",
                params={"test": "test"},
                method="get"
            )

            m.post(requests_mock.ANY, text='{}', status_code=status_code)
            c._Client__call(
                uri="http://example.com",
                params={"test": "test"},
                method="post"
            )

    @requests_mock.Mocker()
    def test_call_fail(self, m):
        """Ensure that failure HTTP response codes fail."""
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
            c.session = requests.Session()

        status_codes = [400, 401, 403, 404, 500]
        caught = 0
        for status_code in status_codes:
            m.get(
                requests_mock.ANY,
                text=json.dumps({'message': 'test'}),
                status_code=400
            )
            try:
                c._Client__call(
                    uri="http://example.com",
                    params=None,
                    method="get"
                )
            except BadRequest:
                caught += 1
        self.assertEqual(len(status_codes), caught)

    @requests_mock.Mocker()
    def test_call_stream_pass(self, m):
        """Ensure that successful HTTP streaming response codes pass."""
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
            c.session = requests.Session()

        for status_code in [200, 201, 202, 301, 302]:
            m.get(requests_mock.ANY, status_code=status_code)
            c._Client__call_stream(
                uri="http://example.com",
                params={"test": "test"},
                method="get"
            )

            m.post(requests_mock.ANY, status_code=status_code)
            c._Client__call_stream(
                uri="http://example.com",
                params={"test": "test"},
                method="post"
            )

    @requests_mock.Mocker()
    def test_call_stream_fail(self, m):
        """Ensure that failure HTTP streaming response codes fail."""
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
            c.session = requests.Session()

        status_codes = [400, 401, 403, 404, 500]
        caught = 0
        for status_code in status_codes:
            m.get(
                requests_mock.ANY,
                text=json.dumps({'message': 'test'}),
                status_code=400
            )
            try:
                c._Client__call_stream(
                    uri="http://example.com",
                    params={"test": "test"},
                    method="get"
                )
            except BadRequest:
                caught += 1
        self.assertEqual(len(status_codes), caught)

    @requests_mock.Mocker()
    def test_custom_json_options(self, m):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
            c.json_options['parse_float'] = Decimal
            m.get(requests_mock.ANY, text=json.dumps({'float': 1.01}))
            r = c._Client__call('http://www.example.com/')
            assert isinstance(r['float'], Decimal)
