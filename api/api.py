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

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def _hashing(self, query_string):
        return hmac.new(
            self.secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
        ).hexdigest()

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _dispatch_request(self, http_method):
        session = requests.Session()
        session.headers.update(
            {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": self.api_key}
        )
        return {
            "GET": session.get,
            "DELETE": session.delete,
            "PUT": session.put,
            "POST": session.post,
        }.get(http_method, "GET")

    # used for sending request that requires the signature
    def _send_signed_request(self, http_method, url_path, payload={}):
        query_string = urlencode(payload, True)
        if query_string:
            query_string = "{}&timestamp={}".format(query_string, self._get_timestamp())
        else:
            query_string = "timestamp={}".format(self._get_timestamp())

        url = (
            self.BASE_URL + url_path + "?" + query_string + "&signature=" + self._hashing(query_string)
        )
        print("{} {}".format(http_method, url))
        params = {"url": url, "params": {}}
        response = self._dispatch_request(http_method)(**params)
        return response.json()

    # used for sending public data request
    def _send_public_request(self, url_path, payload={}):
        query_string = urlencode(payload, True)
        url = self.BASE_URL + url_path
        if query_string:
            url = url + "?" + query_string
        print("{}".format(url))
        response = self._dispatch_request("GET")(url=url)
        return response.json()
    

    #Public requests

    #Get candle stick data for symbol and time interval
    def get_klines(self, symbol, interval):
        response = self._send_public_request("/api/v3/klines", {"symbol": symbol, "interval": interval})
        return response
    
    #Get current ptices
    def get_symbol_price_ticker(self):
        response = self._send_public_request("/api/v3/ticker/price")
        return response
    
    def get_instraments(self):
        response = self._send_public_request("/api/v3/exchangeInfo")
        return response

    
    
    #Private requests

    #Get account information
    def get_account_info(self):
        response = self._send_signed_request("GET", "/api/v3/account")
        return response
    
    def get_instruments(self):
        response = self._send_signed_request("GET", "/api/v3/exchangeInfo")
        return response