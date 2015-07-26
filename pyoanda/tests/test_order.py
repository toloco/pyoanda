from datetime import datetime
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ..order import Order


class OrderClassTest(unittest.TestCase):
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
        with self.assertRaises(TypeError):
            order.check()

    def test_creation_bad_units(self):
        order = Order(
            instrument="GBP_EUR",
            units="bad",
            side="buy",
            type="market"
        )
        with self.assertRaises(TypeError):
            order.check()

    def test_creation_bad_side(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="bad",
            type="market"
        )
        with self.assertRaises(TypeError):
            order.check()

    def test_creation_bad_type(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="sell",
            type="bad"
        )
        with self.assertRaises(TypeError):
            order.check()

    def test_creation_with_type(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="sell",
            type="limit",
            price=10.0,
            expiry=datetime.now()
        )
        order.check()

    def test_creation_with_type_error(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="sell",
            type="limit",
            price=10.0,
        )
        with self.assertRaises(TypeError):
            order.check()

    def test_creation_bad_expiry(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="sell",
            type="limit",
            price=10.0,
            expiry="datetime.now()"
        )
        with self.assertRaises(TypeError):
            order.check()

    def test_creation_bad_price(self):
        order = Order(
            instrument="GBP_EUR",
            units=1,
            side="sell",
            type="limit",
            price="10.0",
            expiry=datetime.now()
        )
        order.check()
