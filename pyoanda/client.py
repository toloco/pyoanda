import requests

from logging import getLogger
from requests.exceptions import RequestException
try:
    from types import NoneType
except ImportError:
    NoneType = type(None)

from .exceptions import BadCredentials, BadRequest


log = getLogger(__name__)


class Client(object):
    API_VERSION = "v1"

    def __init__(
        self,
        environment,
        account_id=None,
        access_token=None,
        json_options=None
    ):
        self.domain, self.domain_stream = environment
        self.access_token = access_token
        self.account_id = account_id
        self.json_options = json_options or {}
        if account_id and not self.get_credentials():
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

    def __session_stablisher(self):
        if not hasattr(self, "session") or not self.session:
            self.session = requests.Session()
            if self.access_token:
                self.session.headers.update(
                    {'Authorization': 'Bearer {}'.format(self.access_token)}
                )

    def __call_raw(self, uri, params=None, method="get", stream=False):
        """ Makes a raw call to the API with minimal processing.

            Parameters
            ----------
            url : string
                The full URL to request.
            params: dict
                A list of parameters to send with the request.  This
                will be sent as data for methods that accept a request
                body and will otherwise be sent as query parameters.
            method : str
                The HTTP method to use.
            stream : bool
                Whether to stream the response.

            Returns a requests.Response object.
        """
        self._Client__session_stablisher()
        # Remove empty params
        if params:
            params = {k: v for k, v in params.items() if v is not None}
        kwargs = {
            "url": uri,
            "verify": True,
            "stream": stream
        }
        if method == "get":
            kwargs["params"] = params
        else:
            kwargs["data"] = params
            
        return getattr(self.session, method)(**kwargs)

    def __call(self, uri, params=None, method="get"):
        """Only returns the response, nor the status_code
        """
        try:
            resp = self.__call_raw(uri, params, method, False)
            rjson = resp.json(**self.json_options)
            assert resp.ok
        except AssertionError:
            msg = "OCode-{}: {}".format(resp.status_code, rjson["message"])
            raise BadRequest(msg)
        except Exception as e:
            msg = "Bad response: {}".format(e)
            log.error(msg, exc_info=True)
            raise BadRequest(msg)
        else:
            return rjson

    def __call_stream(self, uri, params=None, method="get"):
        """Returns an stream response
        """
        try:
            resp = self.__call_raw(uri, params, method, True)
            assert resp.ok
        except AssertionError:
            raise BadRequest(resp.status_code)
        except Exception as e:
            log.error("Bad response: {}".format(e), exc_info=True)
        else:
            return resp

    def get_instruments(self):
        """
            See more:
            http://developer.oanda.com/rest-live/rates/#getInstrumentList
        """
        url = "{0}/{1}/instruments".format(self.domain, self.API_VERSION)
        params = {"accountId": self.account_id}
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
            See more:
            http://developer.oanda.com/rest-live/rates/#getCurrentPrices
        """
        url = "{0}/{1}/prices".format(
            self.domain_stream if stream else self.domain,
            self.API_VERSION
        )
        params = {"accountId": self.account_id, "instruments": instruments}
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
                               weekly_alignment="Monday", start=None,
                               end=None):
        """
            See more:
            http://developer.oanda.com/rest-live/rates/#retrieveInstrumentHistory
        """
        url = "{0}/{1}/candles".format(self.domain, self.API_VERSION)
        params = {
            "accountId": self.account_id,
            "instrument": instrument,
            "candleFormat": candle_format,
            "granularity": granularity,
            "count": count,
            "dailyAlignment": daily_alignment,
            "alignmentTimezone": alignment_timezone,
            "weeklyAlignment": weekly_alignment,
            "start": start,
            "end": end,
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
            See more:
            http://developer.oanda.com/rest-live/orders/#getOrdersForAnAccount
        """
        url = "{0}/{1}/accounts/{2}/orders".format(
            self.domain,
            self.API_VERSION,
            self.account_id
        )
        params = {"instrument": instrument, "count": count}
        try:
            return self._Client__call(uri=url, params=params, method="get")
        except RequestException:
            return False
        except AssertionError:
            return False

    def get_order(self, order_id):
        """
            See more:
            http://developer.oanda.com/rest-live/orders/#getInformationForAnOrder
        """
        url = "{0}/{1}/accounts/{2}/orders/{3}".format(
            self.domain,
            self.API_VERSION,
            self.account_id,
            order_id
        )
        try:
            return self._Client__call(
                uri=url,
                method="get"
            )
        except RequestException:
            return False
        except AssertionError:
            return False

    def create_order(self, order):
        """
            See more:
            http://developer.oanda.com/rest-live/orders/#createNewOrder
        """
        url = "{0}/{1}/accounts/{2}/orders".format(
            self.domain,
            self.API_VERSION,
            self.account_id
        )
        try:
            return self._Client__call(
                uri=url,
                params=order.__dict__,
                method="post"
            )
        except RequestException:
            return False
        except AssertionError:
            return False

    def update_order(self, order_id, order):
        """
            See more:
            http://developer.oanda.com/rest-live/orders/#modifyExistingOrder
        """
        url = "{0}/{1}/accounts/{2}/orders/{3}".format(
            self.domain,
            self.API_VERSION,
            self.account_id,
            order_id
        )
        try:
            return self._Client__call(
                uri=url,
                params=order.__dict__,
                method="patch"
            )
        except RequestException:
            return False
        except AssertionError:
            return False

    def close_order(self, order_id):
        """
            See more:
            http://developer.oanda.com/rest-live/orders/#closeOrder
        """
        url = "{0}/{1}/accounts/{2}/orders/{3}".format(
            self.domain,
            self.API_VERSION,
            self.account_id,
            order_id
        )
        try:
            return self._Client__call(uri=url, method="delete")
        except RequestException:
            return False
        except AssertionError:
            return False

    def get_trades(self):
        """
            See more:
            http://developer.oanda.com/rest-live/trades/#getListOpenTrades
        """
        raise NotImplementedError()

    def get_trade(self):
        """
            See more:
            http://developer.oanda.com/rest-live/trades/#getInformationSpecificTrade
        """
        raise NotImplementedError()

    def update_trade(self):
        """
            See more:
            http://developer.oanda.com/rest-live/trades/#modifyExistingTrade
        """
        raise NotImplementedError()

    def close_trade(self):
        """
            See more:
            http://developer.oanda.com/rest-live/trades/#closeOpenTrade
        """
        raise NotImplementedError()

    def get_positions(self):
        """ Get a list of all open positions.

            See more:
            http://developer.oanda.com/rest-live/positions/#getListAllOpenPositions
        """
        url = "{0}/{1}/accounts/{2}/positions".format(
            self.domain,
            self.API_VERSION,
            self.account_id
        )
        try:
            return self._Client__call(uri=url, method="get")
        except RequestException:
            return False
        except AssertionError:
            return False

    def get_position(self, instrument):
        """ Get the position for an instrument.
            
            Parameters
            ----------
            instrument : string
                The instrument to get the open position for.

            See more:
            http://developer.oanda.com/rest-live/positions/#getPositionForInstrument
        """
        url = "{0}/{1}/accounts/{2}/positions/{3}".format(
            self.domain,
            self.API_VERSION,
            self.account_id,
            instrument
        )
        try:
            return self._Client__call(uri=url, method="get")
        except RequestException:
            return False
        except AssertionError:
            return False

    def close_position(self, instrument):
        """ Close an existing position

            Parameters
            ----------
            instrument : string
                The instrument to close the position for.

            See more:
            http://developer.oanda.com/rest-live/positions/#closeExistingPosition
        """
        url = "{0}/{1}/accounts/{2}/positions/{3}".format(
            self.domain,
            self.API_VERSION,
            self.account_id,
            instrument
        )
        try:
            return self._Client__call(uri=url, method="delete")
        except RequestException:
            return False
        except AssertionError:
            return False

    def get_transactions(self, max_id=None, count=None, instrument=None, ids=None):
        """ Get a list of transactions.

            Parameters
            ----------
            max_id : int
                The server will return transactions with id less than or
                equal to this, in descending order (for pagination).
            count : int
                Maximum number of open transactions to return. Default:
                50. Max value: 500.
            instrument : str
                Retrieve open transactions for a specific instrument
                only. Default: all.
            ids : list
                A list of transactions to retrieve. Maximum number of
                ids: 50.  No other parameter may be specified with the
                ids parameter.

            See more:
            http://developer.oanda.com/rest-live/transaction-history/#getTransactionHistory
            http://developer.oanda.com/rest-live/transaction-history/#transactionTypes
        """
        url = "{0}/{1}/accounts/{2}/transactions".format(
            self.domain,
            self.API_VERSION,
            self.account_id
        )
        params = {
            "maxId": int(max_id) if max_id is not None and max_id > 0 else None,
            "count": int(count) if count is not None and count > 0 else None,
            "instrument": instrument,
            "ids": ','.join([str(x) for x in ids]) if ids else None
        }

        try:
            return self._Client__call(uri=url, params=params, method="get")
        except RequestException:
            return False
        except AssertionError:
            return False


    def get_transaction(self, transaction_id):
        """ Get information on a specific transaction.
            
            Parameters
            ----------
            transaction_id : int
                The id of the transaction to get information on.

            See more:
            http://developer.oanda.com/rest-live/transaction-history/#getInformationForTransaction
            http://developer.oanda.com/rest-live/transaction-history/#transactionTypes
        """
        url = "{0}/{1}/accounts/{2}/transactions/{3}".format(
            self.domain,
            self.API_VERSION,
            self.account_id,
            transaction_id
        )
        try:
            return self._Client__call(uri=url, method="get")
        except RequestException:
            return False
        except AssertionError:
            return False

    def request_transaction_history(self):
        """ Request full account history.

            Submit a request for a full transaction history.  A
            successfully accepted submission results in a response
            containing a URL in the Location header to a file that will
            be available once the request is served. Response for the
            URL will be HTTP 404 until the file is ready. Once served
            the URL will be valid for a certain amount of time.

            See more:
            http://developer.oanda.com/rest-live/transaction-history/#getFullAccountHistory
            http://developer.oanda.com/rest-live/transaction-history/#transactionTypes
        """
        url = "{0}/{1}/accounts/{2}/alltransactions".format(
            self.domain,
            self.API_VERSION,
            self.account_id
        )
        try:
            resp = self.__call_raw(url)
            return resp.headers['location']
        except RequestException:
            return False
        except AssertionError:
            return False

    def create_account(self, currency=None):
        """ Create a new account.

            This call is only available on the sandbox system. Please
            create accounts on fxtrade.oanda.com on our production
            system.

            See more:
            http://developer.oanda.com/rest-sandbox/accounts/#-a-name-createtestaccount-a-create-a-test-account
        """
        url = "{0}/{1}/accounts".format(self.domain, self.API_VERSION)
        params = {"currency": currency}
        try:
            return self._Client__call(uri=url, params=params, method="post")
        except RequestException:
            return False
        except AssertionError:
            return False

    def get_accounts(self, username=None):
        """ Get a list of accounts owned by the user.

            Parameters
            ----------
            username : string
                The name of the user. Note: This is only required on the
                sandbox, on production systems your access token will
                identify you.

            See more:
            http://developer.oanda.com/rest-sandbox/accounts/#-a-name-getaccountsforuser-a-get-accounts-for-a-user
        """
        url = "{0}/{1}/accounts".format(self.domain, self.API_VERSION)
        params = {"username": username}
        try:
            return self._Client__call(uri=url, params=params, method="get")
        except RequestException:
            return False
        except AssertionError:
            return False
