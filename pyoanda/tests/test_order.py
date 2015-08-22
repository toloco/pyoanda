from datetime import datetime
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ..order import Order


class OrderClassTest(unittest.TestCase):

    def fail(self, order):
        with self.assertRaises(TypeError):
            assert order.check()

    def test_creation(self):
        order = Order(
            instrument="GBP_EUR",
            units=11,
            side="buy",
            type="market"
        )
        assert order.check()

    def test_creation_bad_param(self):
        order = Order(
            instrument="GBP_EUR",
            units=11,
            side="buy",
            type="market",
            bad="param"
        )
        self.fail(order)

    def test_creation_bad_units(self):
        order = Order(
            instrument="GBP_EUR",
            units="bad",
            side="buy",
            type="market"
        )
        self.fail(order)

    def test_creation_bad_side(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="bad",
            type="market"
        )
        self.fail(order)

    def test_creation_bad_type(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="sell",
            type="bad"
        )
        self.fail(order)

    def test_creation_with_type(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="sell",
            type="limit",
            price=10.0,
            expiry=datetime.now()
        )
        assert order.check()

    def test_creation_with_type_error(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="sell",
            type="limit",
            price=10.0,
        )
        self.fail(order)

    def test_creation_bad_expiry(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="sell",
            type="limit",
            price=10.0,
            expiry="datetime.now()"
        )
        self.fail(order)

    def test_creation_bad_price(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="sell",
            type="limit",
            price="10.0",
            expiry=datetime.now()
        )
        assert order.check()
