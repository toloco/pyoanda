from pyoanda.exceptions import BadRequest

from .integration_test_case import IntegrationTestCase


class TestOrderAPI(IntegrationTestCase):
    def test_get_orders(self):
        assert self.client.get_orders()

    def test_get_order(self):
        order = self.build_order()
        result = self.client.create_order(order)
        assert self.client.get_order(result['orderOpened']['id'])
        assert self.client.get_order(order_id=result['orderOpened']['id'])

    def test_create_order(self):
        order = self.build_order()
        assert self.client.create_order(order)

    def test_update_order(self):
        order = self.build_order()
        result = self.client.create_order(order)
        assert self.client.update_order(result['orderOpened']['id'], order)

    def test_close_order(self):
        order = self.build_order()
        result = self.client.create_order(order)
        assert self.client.close_order(result['orderOpened']['id'])

        with self.assertRaises(BadRequest):
            # Cannot close twice
            self.client.close_order(result['orderOpened']['id'])

        with self.assertRaises(BadRequest):
            # No longer in orders once closed
            self.client.get_order(result['orderOpened']['id'])
