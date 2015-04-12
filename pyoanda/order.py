from datetime import datetime
try:
    from types import NoneType
except ImportError:
    NoneType = type(None)


class Order(object):
    __allowed = ("instrument", "units", "side", "type", "expiry", "price",
                 "lowerBound", "upperBound", "stopLoss", "takeProfit",
                 "trailingStop")
    __requiered = ("instrument", "units", "side", "type")
    __side = ("sell", "buy")
    __type = ("limit", "stop", "marketIfTouched", "market")

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def check(self):
        """
        - Instrument:* Required Instrument to open the order on.
        - Units: Required The number of units to open order for.
        - Side: Required Direction of the order, either ‘buy’ or ‘sell’.
        - Type: Required The type of the order ‘limit’, ‘stop’, ‘marketIfTouched’ or ‘market’.
        - Expiry: Required If order type is ‘limit’, ‘stop’, or ‘marketIfTouched’. The order expiration time in UTC. The value specified must be in a valid datetime format.
        - Price: Required If order type is ‘limit’, ‘stop’, or ‘marketIfTouched’. The price where the order is set to trigger at.
        - LowerBound: Optional The minimum execution price.
        - UpperBound: Optional The maximum execution price.
        - StopLoss: Optional The stop loss price.
        - TakeProfit: Optional The take profit price.
        - TrailingStop: Optional The trailing stop distance in pips, up to one decimal place.
        """
        for k, v in iter(self.__dict__.items()):
            if k not in self.__allowed:
                raise TypeError("Parameter not allowed {}".format(k))

        for k in self.__requiered:
            if k not in self.__dict__:
                raise TypeError("Requiered parameter not found {}".format(k))

        if not isinstance(self.units, (int, float)):
            msg = "Unit must be either int or float, '{}'' found".format(
                type(self.units))
            raise TypeError(msg)

        if self.side not in self.__side:
            msg = "Side must be in {1}, '{0}' found".format(
                self.side, self.__side)
            raise TypeError(msg)

        if self.type not in self.__type:
            msg = "Type must be in {1}, '{0}' found".format(
                self.type, self.__type)
            raise TypeError(msg)

        if not self.type == "market" and (
           not hasattr(self, "expiry") or not hasattr(self, "price")):
            msg = "As type is {}, expiry and price must be provided".format(
                self.type)
            raise TypeError(msg)
        if hasattr(self, "expiry") and not isinstance(self.expiry, datetime):
            msg = "Expiry must be {1}, '{0}' found".format(
                type(self.expiry), datetime)
            raise TypeError(msg)

        if hasattr(self, "price") and not isinstance(self.price, (int, float)):
            msg = "Expiry must be int or float, '{0}' found".format(
                type(self.price))
            raise TypeError(msg)

        return True
