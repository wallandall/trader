class Instrument:
    def __init__(
        self,
        symbol,
        status,
        baseAsset,
        quoteAsset,
        baseAssetPrecision,
        quotePrecision,
        quoteAssetPrecision,
    ):
        self.symbol = symbol
        self.status = status
        self.baseAsset = baseAsset
        self.quoteAsset = quoteAsset
        self.baseAssetPrecision = baseAssetPrecision
        self.quotePrecision = quotePrecision
        self.quoteAssetPrecision = quoteAssetPrecision

    def __repr__(self):
        return str(vars(self))

    @classmethod
    def FromApiObject(cls, ob):
        return Instrument(
            ob["symbol"],
            ob["status"],
            ob["baseAsset"],
            ob["quoteAsset"],
            ob["baseAssetPrecision "],
            ob["quotePrecision"],
            ob["quoteAssetPrecision"],
        )
