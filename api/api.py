import requests
import hashlib
import hmac
import time

from dotenv import dotenv_values

config = dotenv_values(".env")



class TraderApi:
    BASE_URL = config["BASE_URL"]
    KEY = config["API_KEY"]
    SECRET= config["SECRET_KEY"]
    def __init__(self):
        self.api_key = self.KEY
        self.api_secret = self.SECRET

    def _generate_signature(self, params):
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature

    def _make_request(self, method, endpoint, params=None, headers=None):
        url = self.BASE_URL + endpoint
        headers = headers or {}
        params = params or {}

        if method == 'GET':
            response = requests.get(url, headers=headers, params=params)
        elif method == 'POST':
            response = requests.post(url, headers=headers, params=params)
        else:
            raise ValueError(f'Unsupported HTTP method: {method}')

        response.raise_for_status()
        return response.json()

    def get_account_info(self):
        endpoint = '/account'
        params = {
            'timestamp': int(time.time() * 1000),
            'recvWindow': 5000,
            'apiKey': self.api_key
        }
        params['signature'] = self._generate_signature(params)
        headers = {'X-MBX-APIKEY': self.api_key}

        return self._make_request('GET', endpoint, params, headers)

    def get_recent_trades(self, symbol, limit=100):
        endpoint = '/trades'
        params = {
            'symbol': symbol,
            'limit': limit
        }

        return self._make_request('GET', endpoint, params)

