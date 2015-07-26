# -*- coding: UTF-8 -*-
from datetime import datetime
from decimal import Decimal, InvalidOperation
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
        Logic extracted from:
        http://developer.oanda.com/rest-live/orders/#createNewOrder
        """
        for k in iter(self.__dict__.keys()):
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

        if hasattr(self, "price"):
            try:
                Decimal(self.price)
            except InvalidOperation:
                msg = "Expiry must be int or float, '{0}' found".format(
                    type(self.price))
                raise TypeError(msg)

        return True
