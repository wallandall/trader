import json
import pandas as pd
from models.instrument import Instrument

class InstrumentCollection:
    FILENAME="instruments.json"
    API_KEYS=['symbol', 'baseAsset', 'quoteAsset']

    def __init__(self):
        self.instraments_dict={}

    def LoadInstruments(self, path):
        self.instraments_dict={}
        fileName=f"{path}/{self.FILENAME}"
        with open(fileName, "r") as f:
            data = json.loads(f.read())
            for k, v in data.items():
                self.instruments_dict[k]=Instrument.FromApiObject(v)
    
    def CreateFile(self, data, path):
        if data is None:
            print("Instrument file creation failed")
            return
        
        instruments_dict = {}
        for symbol_info in data['symbols']:
            key = symbol_info.get('symbol')
            if key:
                instruments_dict[key] = {k: symbol_info.get(k) for k in self.API_KEYS}

        fileName = f"{path}/{self.FILENAME}"
        with open(fileName, "w") as f:
            json.dump(instruments_dict, f, indent=2)



    def PrintInstruments(self):
        [print(k,v) for k,v in self.instruments_dict.items()]
        print(len(self.instruments_dict.keys()), "instruments")


instrumentCollection = InstrumentCollection()