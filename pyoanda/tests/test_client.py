try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from unittest import mock
except ImportError:
    import mock

import requests
from requests.exceptions import RequestException

from ..client import Client
from ..order import Order
from ..exceptions import BadCredentials, BadRequest


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

    def test_call_pass(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
            c.session = requests.Session()
        obj = mock
        setattr(obj, "json", lambda: 1)
        setattr(obj, "ok", True)
        with mock.patch.object(c.session, 'get', return_value=obj):
            c._Client__call(uri="test", params={"test": "test"}, method="get")

        with mock.patch.object(c.session, 'post', return_value=obj):
            c._Client__call(uri="test", params={"test": "test"}, method="post")

    def test_call_fail(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
            c.session = requests.Session()
        obj = mock
        setattr(obj, "json", lambda: {"message": "Bad request"})
        setattr(obj, "status_code", 400)
        setattr(obj, "ok", False)
        with mock.patch.object(c.session, 'get', return_value=obj):
            with self.assertRaises(BadRequest):
                c._Client__call(uri="test", params=None, method="get")

    def test_call_stream_pass(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
            c.session = requests.Session()
        obj = mock
        setattr(obj, "json", lambda: 1)
        setattr(obj, "ok", True)
        with mock.patch.object(c.session, 'get', return_value=obj):
            c._Client__call_stream(
                uri="test",
                params={"test": "test"},
                method="get"
            )

        with mock.patch.object(c.session, 'post', return_value=obj):
            c._Client__call_stream(
                uri="test",
                params={"test": "test"},
                method="post"
            )

    def test_call_stream_fail(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
            c.session = requests.Session()
        obj = mock
        setattr(obj, "json", lambda: {"message": "Bad request"})
        setattr(obj, "status_code", 400)
        setattr(obj, "ok", False)
        with mock.patch.object(c.session, 'get', return_value=obj):
            with self.assertRaises(BadRequest):
                c._Client__call_stream(uri="test", params={"test": "test"}, method="get")

    def test_session_stablisher(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            c = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )
            c._Client__session_stablisher()


class TestInstrumentsAPI(unittest.TestCase):
    def setUp(self):
        with mock.patch.object(Client, 'get_credentials', return_value=True):
            self.client = Client(
                ("http://mydomain.com", "http://mystreamingdomain.com"),
                "my_account",
                "my_token"
            )

    def test_get_instruments_pass(self):
        with mock.patch.object(
            Client, '_Client__call',
            return_value={"message": "good one"}
        ):
            assert self.client.get_instruments()

    def test_get_prices(self):
        with mock.patch.object(
            Client, '_Client__call',
            return_value={"message": "good one"}
        ):
            assert self.client.get_prices(instruments="EUR_GBP", stream=False)


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

    def test_order_creation(self):
        order = Order()
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.create_order(order)

    def test_get_orders(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_orders()

    def test_get_order(self):
        with mock.patch.object(Client, '_Client__call', return_value=True):
            assert self.client.get_order(1)
        pass

    def test_create_order(self):
        pass

    def test_update_order(self):
        pass

    def test_close_order(self):
        pass
