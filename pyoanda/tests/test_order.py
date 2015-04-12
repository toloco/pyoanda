try:
    import unittest2 as unittest
except ImportError:
    import unittest

from ..order import Order


class OrderClassTest(unittest.TestCase):
    def test_creation(self):
        order = Order(instrument="GBP_EUR")
        assert order.check()

    def test_creation_error(self):
        order = Order(bad_param="dont care")
        with self.assertRaises(TypeError):
            order.check()
