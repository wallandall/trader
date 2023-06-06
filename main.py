from api.api import TraderApi
from infrastructure.instrument_collection import instrumentCollection
from dotenv import dotenv_values

config = dotenv_values(".env")

BASE_URL = config["BASE_URL"]
KEY = config["API_KEY"]
SECRET = config["SECRET_KEY"]

if __name__ == '__main__':

    api = TraderApi(KEY, SECRET)

    #data = api.get_account_info()
    #data = api.get_klines("BTCUSDT","1d")
    #data = api.get_symbol_price_ticker()
    ##data = api.get_instraments()
    ##print(data)
    #[print(x['symbol']) for x in data]
    ##instrumentCollection.LoadInstruments("./data")
    ##instrumentCollection.PrintInstruments()
    instrumentCollection.CreateFile(api.get_instraments(), "./data")