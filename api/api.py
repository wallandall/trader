import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode

from dotenv import dotenv_values

config = dotenv_values(".env")


class TraderApi:
    BASE_URL = config["BASE_URL"]
    KEY = config["API_KEY"]
    SECRET = config["SECRET_KEY"]

    def __init__(self):
        self.api_key = self.KEY
        self.api_secret = self.SECRET

    # def _generate_signature(self, params):
    #     query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    #     signature = hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    #     return signature

    # def _make_request(self, method, endpoint, params=None, headers=None):
    #     url = self.BASE_URL + endpoint
    #     headers = headers or {}
    #     params = params or {}

    #     if method == 'GET':
    #         response = requests.get(url, headers=headers, params=params)
    #     elif method == 'POST':
    #         response = requests.post(url, headers=headers, params=params)
    #     else:
    #         raise ValueError(f'Unsupported HTTP method: {method}')

    #     response.raise_for_status()
    #     return response.json()

    # def get_account_info(self):
    #     endpoint = '/api/account'
    #     params = {
    #         'timestamp': int(time.time() * 1000),
    #         'recvWindow': 5000,
    #         'apiKey': self.api_key
    #     }
    #     params['signature'] = self._generate_signature(params)
    #     headers = {'X-MBX-APIKEY': self.api_key}

    #     return self._make_request('GET', endpoint, params, headers)

    # def get_recent_trades(self, symbol, limit=100):
    #     endpoint = '/trades'
    #     params = {
    #         'symbol': symbol,
    #         'limit': limit
    #     }

    #     return self._make_request('GET', endpoint, params)

    def _hashing(self, query_string):
        return hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _dispatch_request(self, http_method):
        session = requests.Session()
        session.headers.update(
            {
                "Content-Type": "application/json;charset=utf-8",
                "X-MBX-APIKEY": self.api_key,
            }
        )
        return{
            "GET":session.get,
            "DELET":session.delete,
            "PUT":session.put,
            "POST":session.post
        }.get(http_method, "GET")
    
    def _send_signed_request(self, http_method, url_path, payload={}):
        query_string = urlencode(payload, True)
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self._get_timestamp())
        else:
            query_string = "timestamp={}".format( self._get_timestamp())
        signature = self._hashing(query_string)
        url = (
            self.BASE_URL + url_path + "?" + query_string + "&signature=" + signature
        )
        print("{} {}".format(http_method, url))
        params = {"url": url, "params": {}}
        response = self._dispatch_request(http_method)(**params)
        return response.json()
    
    def _send_public_request(self, url_path, payload={}):
      query_string = urlencode(payload, True)
      url = self.BASE_URL + url_path
      if query_string:
        url = url + "?" + query_string
      print("{}".format(url))
      response = self._dispatch_request("GET")(url=url)
      return response.json()
    
    #################################################################
    ##                      Public API Queries                     ##
    #################################################################
    def get_klines(self,symbol, interval):
        response = self._send_public_request(
            "/api/v3/klines", {"symbol": symbol, "interval": interval}
        )
        return response

    #################################################################
    ##                      Private API Queries                    ##
    #################################################################
    def get_account_info(self):
        response = self._send_signed_request("GET", "/api/v3/account")
        return response