import requests
import json
import yaml
import sys

from requests.exceptions import RequestException


def create_stream(uri, access,):

    access = config["access"]

    instruments = "EUR_GBP"
    url = "https://{}/v1/prices".format(OANDA_DOMAIN)
    headers = {'Authorization' : 'Bearer {}'.format(access["access_token"])}
    params = {'instruments' : instruments, 'accountId' : access["account_id"]}
    req = requests.Request('GET', url, headers = headers, params = params)

    with requests.Session() as s:
        resp = s.send(req.prepare(), stream = True, verify = False)
        assert resp.status_code == 200
        return resp

def by_api(uri, access_token, params = None, method="GET"):

    headers = {'Authorization' : 'Bearer {}'.format(access_token)}
    req = requests.Request(method, uri, headers = headers, params = params)

    with requests.Session() as s:
        resp = s.send(req.prepare(), verify = False)
        if resp.status_code == 200:
            return resp
        else:
            raise RequestException()
