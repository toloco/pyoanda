__version__ = "1.021"


try:
    from .client import Client
    from .order import Order
except ImportError:
    pass


# OANDA API URLS
SANDBOX = (
    "http://api-sandbox.oanda.com",
    "http://stream-sandbox.oanda.com"
)
PRACTICE = (
    "https://api-fxpractice.oanda.com",
    "https://stream-fxpractice.oanda.com"
)
TRADE = (
    "https://api-fxtrade.oanda.com",
    "https://stream-fxtrade.oanda.com"
)
