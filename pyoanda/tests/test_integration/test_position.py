try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pyoanda.exceptions import BadRequest

from .integration_test_case import IntegrationTestCase


class TestPositionAPI(IntegrationTestCase):
    def test_get_positions(self):
        self.client.get_positions()

    def test_get_position(self):
        order = self.build_order(immediate=True)
        self.client.create_order(order)
        assert self.client.get_position('GBP_USD')
        assert self.client.get_position(instrument='GBP_USD')

    @unittest.skip("Failing due to Oanda bug, HTTP 500 on close")
    def test_close_position(self):
        order = self.build_order(immediate=True)
        self.client.create_order(order)
        assert self.client.close_position('GBP_USD')

        # cannot close twice
        with self.assertRaises(BadRequest):
            assert self.client.close_position('GBP_USD')

        # cannot get position if closed
        with self.assertRaises(BadRequest):
            assert self.client.get_position('GBP_USD')
