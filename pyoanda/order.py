try:
    from types import NoneType
except ImportError:
    NoneType = type(None)


class Order(object):
    __allowed = ("instrument", "units", "side", "type", "expiry", "price",
                 "lowerBound", "upperBound", "stopLoss", "takeProfit",
                 "trailingStop")

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def check(self):
        """
        instrument:* Required Instrument to open the order on.
        units: Required The number of units to open order for.
        side: Required Direction of the order, either ‘buy’ or ‘sell’.
        type: Required The type of the order ‘limit’, ‘stop’, ‘marketIfTouched’ or ‘market’.
        expiry: Required If order type is ‘limit’, ‘stop’, or ‘marketIfTouched’. The order expiration time in UTC. The value specified must be in a valid datetime format.
        price: Required If order type is ‘limit’, ‘stop’, or ‘marketIfTouched’. The price where the order is set to trigger at.
        lowerBound: Optional The minimum execution price.
        upperBound: Optional The maximum execution price.
        stopLoss: Optional The stop loss price.
        takeProfit: Optional The take profit price.
        trailingStop: Optional The trailing stop distance in pips, up to one decimal place.
        """
        for k, v in iter(self.__dict__.items()):
            if k not in self.__allowed:
                raise TypeError("Bad parameter {}".format(k))

        return True
