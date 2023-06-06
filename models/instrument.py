class Instrument:
    def __init__(self, 
                  symbol, 
                  base_asset, 
                  quote_asset):
        self.symbol=symbol 
        self.base_asset=base_asset
        self.quote_asset=quote_asset
    
    def __repr__(self):
       return str(vars(self))
    
    @classmethod
    def FromApiObject(cls, ob):
        return Instrument(ob['symbol'], ob['baseAsset'], ob['quoteAsset'])
   