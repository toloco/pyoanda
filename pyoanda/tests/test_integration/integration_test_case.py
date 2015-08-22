from datetime import datetime, timedelta
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pyoanda import SANDBOX
from pyoanda.client import Client
from pyoanda.order import Order


class IntegrationTestCase(unittest.TestCase):

    # Keep this as it will be share between all tests cases, prevent to over
    # use as this literaly creates new users (I expext the use to be wipeout)
    client = Client(SANDBOX)
    user = client.create_account(currency="GBP")
    client.account_id = user['accountId']

    def build_order(self, immediate=False):
        """ Build an order to be used with create_order.

            Building an order is commonly required in the integration
            tests, so this makes it easy.

            Parameters
            ----------
            immediate: bool
                Whether to place an order that will be met immediately
                or not; this is achieved by examining current prices and
                bidding well below for non-immediate or by placing a
                market order for immediate.

            Returns an Order
        """
        if immediate:
            return Order(
                instrument="GBP_USD",
                units=1,
                side="buy",
                type="market"
            )

        expiry = datetime.utcnow() + timedelta(minutes=1)
        prices = self.client.get_prices("GBP_USD", False)
        price = prices['prices'][0]
        at = round(price['bid'] * 0.9, 5)

        # order must not be met straight away, otherwise we can't get it back
        return Order(
            instrument="GBP_USD",
            units=1,
            side="buy",
            type="limit",
            price=at,
            expiry=expiry.isoformat()
        )
