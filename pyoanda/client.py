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
    SIDES = ("buy", "sell")
    ORDER_TYPE = ("limit", "stop", "marketIfTouched", "market")
    
    def __init__(self, domain, domain_stream, account_id, access_token):
        self.domain = domain
        self.domain_stream = domain_stream
        self.access_token = access_token
        self.account_id = account_id
        if not self._Client__get_credentials():
            raise BadCredentials()

    def __get_credentials(self):
        """
            See more: http://developer.oanda.com/rest-live/accounts/
        """
        url = "{0}/{1}/accounts/{2}".format(self.domain, self.VERSION, self.account_id)
        try:
            response = self._Client__call(uri=url)
            assert len(response) > 0
            return response
        except RequestException:
            return False
        except AssertionError:
            return False

    def __call(self, uri, params = None, method="get"):
        if not hasattr(self, "session") or not self.session:
            self.session = requests.Session()
            self.session.headers.update({'Authorization' : 'Bearer {}'.format(self.access_token)})
        try:
            resp = getattr(self.session, method)(uri, params=params, verify=True, stream = False)
            assert resp.status_code == 200
        except AssertionError:
            raise BadRequest()
        except Exception as e:
            log.error("Bad response: {}".format(e), exc_info=True)
        else:
            return resp.json()

    def __call_stream(self, uri, params = None, method="get"):
        """Returns an stream response
        """
        if not hasattr(self, "session") or not self.session:
            self.session = requests.Session()
            self.session.headers.update({'Authorization' : 'Bearer {}'.format(self.access_token)})
        try:
            resp = getattr(self.session, method)(uri, params=params, verify=True, stream = True)
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
        url = "{0}/{1}/instruments".format(self.domain, self.VERSION)
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
        url = "{0}/{1}/prices".format(self.domain_stream if stream else self.domain, self.VERSION)
        params = {"accountId" : self.account_id, "instruments": instruments}
        try:
            if stream:
                return self._Client__call_stream(uri=url, params=params, method="get")
            else:
                return self._Client__call(uri=url, params=params, method="get")
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
        url = "{0}/{1}/candles".format(self.domain, self.VERSION)
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

    def get_account_orders(self, instrument=None, count=50):
        """
            See more: http://developer.oanda.com/rest-live/orders/#getOrdersForAnAccount
        """
        url = "{0}/{1}/accounts/{2}/orders".format(self.domain, self.VERSION,self.account_id)
        params = {
            "instrument":instrument, 
            "count":count
        }
        # Remove empty params
        params = {k: v for k, v in params.items() if v}
        try:
            return self._Client__call(uri=url, params=params, method="get")
        except RequestException:
            return False
        except AssertionError:
            return False

    def create_order(self, instrument, units, side="buy", order_type="market",
                     expiry=None, price=None, lowerBound=None, upperBound=None, stopLoss=0, takeProfit=0, trailingStop=0):
        """
            See more: http://developer.oanda.com/rest-live/orders/#createNewOrder
        """
        url = "{0}/{1}/accounts/{2}/orders".format(self.domain, self.API_VERSION,self.account_id)

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
            "type":(str, ("limit", "stop", "marketIfTouched", "market")),
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







