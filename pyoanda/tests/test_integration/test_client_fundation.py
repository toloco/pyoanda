from pyoanda import SANDBOX
from pyoanda.client import Client
from pyoanda.exceptions import BadRequest


from .integration_test_case import IntegrationTestCase


class TestClientFoundation(IntegrationTestCase):
    def test_connect_pass(self):
        assert self.client.get_credentials()

    def test_connect_fail(self):
        with self.assertRaises(BadRequest):
            Client(SANDBOX, 999999999)
