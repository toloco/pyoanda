import requests
import datetime

from logging import getLogger
from requests.exceptions import RequestException
from enum import Enum
try:
    from types import NoneType
except ImportError:
    NoneType = type(None)

from .exceptions import BadCredentials, BadRequest
from .utils.type_checker import type_checker


log = getLogger(__name__)

class Client(object):
    API_VERSION = "v1"
    
    def __init__(self, environment, account_id, access_token):
        self.domain, self.domain_stream = environment
        self.access_token = access_token
        self.account_id = account_id
        if not self.get_credentials():
            raise BadCredentials()

    def get_credentials(self):
        """
            See more: http://developer.oanda.com/rest-live/accounts/
        """
        url = "{0}/{1}/accounts/{2}".format(
            self.domain,
            self.API_VERSION,
            self.account_id
        )
        try:
            response = self._Client__call(uri=url)
            assert len(response) > 0
            return response
        except RequestException:
            return False
        except AssertionError:
            return False

    def __call(self, uri, params = None, method="get"):
        """Only returns the response, nor the status_code
        """
        if not hasattr(self, "session") or not self.session:
            self.session = requests.Session()
            self.session.headers.update(
                {'Authorization' : 'Bearer {}'.format(self.access_token)}
            )
        # Remove empty params
        params = {k: v for k, v in params.items() if v}
        kwargs = {
            "url": uri,
            "verify": True,
            "stream": False
        }
        if method == "get":
            kwargs["params"] = params
        else:
            kwargs["data"] = params
        try:
            resp = getattr(self.session, method)(**kwargs)
            rjson = resp.json()
            assert resp.status_code == 200
        except AssertionError:
            raise BadRequest("OCode-{}: {}".format(rjson["code"], rjson["message"]))
        except Exception as e:
            log.error("Bad response: {}".format(e), exc_info=True)
        else:
            return rjson

    def __call_stream(self, uri, params = None, method="get"):
        """Returns an stream response
        """
        if not hasattr(self, "session") or not self.session:
            self.session = requests.Session()
            self.session.headers.update(
                {'Authorization' : 'Bearer {}'.format(self.access_token)}
            )
        # Remove empty params
        params = {k: v for k, v in params.items() if v}
        kwargs = {
            "url": uri,
            "verify": True,
            "stream": True
        }
        if method == "get":
            kwargs["params"] = params
        else:
            kwargs["data"] = params
        try:
            resp = getattr(self.session, method)(**kwargs)
            assert resp.status_code == 200
        except AssertionError:
            raise BadRequest()
        except Exception as e:
            log.error("Bad response: {}".format(e), exc_info=True)
        else:
            return resp

    def get_instruments(self):
        """
            See more: http://developer.oanda.com/rest-live/rates/#getInstrumentList
        """
        url = "{0}/{1}/instruments".format(self.domain, self.API_VERSION)
        params = {"accountId" : self.account_id}
        try:
            response = self._Client__call(uri=url, params=params)
            assert len(response) > 0
            return response
        except RequestException:
            return False
        except AssertionError:
            return False

    def get_prices(self, instruments, stream=True):
        """
            See more: http://developer.oanda.com/rest-live/rates/#getCurrentPrices
        """
        url = "{0}/{1}/prices".format(
            self.domain_stream if stream else self.domain,
            self.API_VERSION
        )
        params = {"accountId" : self.account_id, "instruments": instruments}
        try:
            if stream:
                return self._Client__call_stream(
                    uri=url,
                    params=params,
                    method="get"
                )
            else:
                return self._Client__call(
                    uri=url,
                    params=params,
                    method="get"
                )
        except RequestException:
            return False
        except AssertionError:
            return False

    def get_instrument_history(self, instrument, candle_format, granularity,
                               count=500, daily_alignment=None,
                               alignment_timezone=None,
                               weekly_alignment="Monday", start=None, end=None
                              ):
        """
            See more: http://developer.oanda.com/rest-live/rates/#retrieveInstrumentHistory
        """
        url = "{0}/{1}/candles".format(self.domain, self.API_VERSION)
        params = {
            "accountId" : self.account_id,
            "instrument":instrument, 
            "candleFormat":candle_format,
            "granularity":granularity,
            "count":count,
            "dailyAlignment":daily_alignment,
            "alignmentTimezone":alignment_timezone,
            "weeklyAlignment":weekly_alignment,
            "start":start,
            "end":end,
        }
        # Remove empty params
        params = {k: v for k, v in params.items() if v}
        try:
            return self._Client__call(uri=url, params=params, method="get")
        except RequestException:
            return False
        except AssertionError:
            return False

    def get_orders(self, instrument=None, count=50):
        """
            See more: http://developer.oanda.com/rest-live/orders/#getOrdersForAnAccount
        """
        url = "{0}/{1}/accounts/{2}/orders".format(
            self.domain,
            self.API_VERSION,
            self.account_id
        )
        params = {
            "instrument":instrument, 
            "count":count
        }
        try:
            return self._Client__call(uri=url, params=params, method="get")
        except RequestException:
            return False
        except AssertionError:
            return False

    def get_order(self, order_id):
        """
            Se more: http://developer.oanda.com/rest-live/orders/#getInformationForAnOrder
        """
        raise NotImplementedError()

    def create_order(self, instrument, units, side="buy", order_type=None,
                     expiry=None, price=None, lowerBound=None, upperBound=None,
                     stopLoss=0, takeProfit=0, trailingStop=0
                    ):
        """
            See more: http://developer.oanda.com/rest-live/orders/#createNewOrder
        """
        url = "{0}/{1}/accounts/{2}/orders".format(
            self.domain,
            self.API_VERSION,
            self.account_id
        )

        params = {
            "instrument":instrument, 
            "units": units,
            "side": side,
            "type": order_type,
            "expiry": expiry,
            "price": price,
            "lowerBound": lowerBound,
            "upperBound": upperBound,
            "stopLoss": stopLoss,
            "takeProfit": takeProfit,
            "trailingStop": trailingStop
        }

        checker = {
            "instrument": (str,),
            "units": ((float, int),),
            "side":(str, ("buy", "sell")),
            "type":((NoneType, str), (None, "limit", "stop", "marketIfTouched", "market")),
            "expiry":((NoneType, datetime),),
            "price":((NoneType, float, int),),
            "lowerBound":((NoneType, float, int),),
            "upperBound":((NoneType, float, int),),
            "stopLoss":((NoneType, int),),
            "takeProfit":((NoneType, int),),
            "trailingStop":((NoneType, int),)
        } 
        try:
            type_checker(params, checker)
        except TypeError as e:
            raise BadRequest(e.__str__)

        # Remove empty params
        params = {k: v for k, v in params.items() if v}
        try:
            return self._Client__call(uri=url, params=params, method="post")
        except RequestException:
            return False
        except AssertionError:
            return False

    def update_order(self, order_id,units, side="buy", order_type=None,
                     expiry=None, price=None, lowerBound=None, upperBound=None,
                     stopLoss=0, takeProfit=0, trailingStop=0
                    ):
        """
            Se more: http://developer.oanda.com/rest-live/orders/#modifyExistingOrder
        """
        raise NotImplementedError()

    def close_order(self, order_id):
        """
            Se more: http://developer.oanda.com/rest-live/orders/#closeOrder
        """
        raise NotImplementedError()

    def get_trades(self):
        """
            Se more: http://developer.oanda.com/rest-live/trades/#getListOpenTrades
        """
        raise NotImplementedError()

    def get_trade(self):
        """
            Se more: http://developer.oanda.com/rest-live/trades/#getInformationSpecificTrade
        """
        raise NotImplementedError()

    def update_trade(self):
        """
            Se more: http://developer.oanda.com/rest-live/trades/#modifyExistingTrade
        """
        raise NotImplementedError()

    def close_trade(self):
        """
            Se more: http://developer.oanda.com/rest-live/trades/#closeOpenTrade
        """
        raise NotImplementedError()

    def get_positions(self):
        """
            Se more: http://developer.oanda.com/rest-live/positions/#getListAllOpenPositions
        """
        raise NotImplementedError()  

    def get_position(self):
        """
            Se more: http://developer.oanda.com/rest-live/positions/#getPositionForInstrument
        """
        raise NotImplementedError()

    def close_position(self):
        """
            Se more: http://developer.oanda.com/rest-live/positions/#closeExistingPosition
        """
        raise NotImplementedError()


    def get_transactions(self):
        """
            Se more: http://developer.oanda.com/rest-live/transaction-history/#getTransactionHistory
                     http://developer.oanda.com/rest-live/transaction-history/#transactionTypes
        """
        raise NotImplementedError()

    def get_transaction(self):
        """
            Se more: http://developer.oanda.com/rest-live/transaction-history/#getInformationForTransaction
                     http://developer.oanda.com/rest-live/transaction-history/#transactionTypes
        """
        raise NotImplementedError()

    def get_account_transaction_history(self):
        """
            Se more: http://developer.oanda.com/rest-live/transaction-history/#getFullAccountHistory
                     http://developer.oanda.com/rest-live/transaction-history/#transactionTypes
        """
        raise NotImplementedError()

