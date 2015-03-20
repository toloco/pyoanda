import requests
from logging import getLogger
from requests.exceptions import RequestException

from .exceptions import BadCredentials, BadRequest

log = getLogger(__name__)

class Client(object):
    VERSION = "v1"
    
    def __init__(self, domain, domain_stream, account_id, access_token):
        self.domain = domain
        self.domain_stream = domain_stream
        self.access_token = access_token
        self.account_id = account_id
        self.my_account = self._Client__get_credentials()
        if not self.my_account:
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
            response = getattr(self.session, method)(uri, params=params, verify=True, stream = False)
            assert response.status_code == 200
        except AssertionError:
            raise BadRequest()
        except Exception as e:
            log.error("Bad response: {}".format(e), exc_info=True)
        else:
            return response.json()

    def __call_stream(self, uri, params = None, method="get"):
        """Returns an stream response
        """
        if not hasattr(self, "session") or not self.session:
            self.session = requests.Session()
            self.session.headers.update({'Authorization' : 'Bearer {}'.format(self.access_token)})
        try:
            response = getattr(self.session, method)(uri, params=params, verify=False, stream = True)
            assert response.status_code == 200
        except AssertionError:
            raise BadRequest()
        except Exception as e:
            log.error("Bad response: {}".format(e), exc_info=True)
        else:
            return response

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
