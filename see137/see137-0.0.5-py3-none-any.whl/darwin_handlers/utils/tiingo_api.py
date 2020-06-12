import time
import maya
import datetime as dateeee
from maya import MayaDT
from patman import Patman
from typing import Any

class TiingoAPI(Patman):
    def __init__(self, host:str, token=""):
        super().__init__(host)
        self._token = token
        self._period = ""
        self._freq = "1min"
    
    @property
    def token(self):
        return self._token
    
    @token.setter
    def token(self, _token):
        self._token = _token
    
    @property
    def freq(self):
        return self._freq
    
    @freq.setter
    def freq(self, _freq):
        self._freq = _freq
    
    def realtime_ticker(self, ticker:str):
        url = f"iex?tickers={ticker}&token={self.token}"
        call = self._create_url_call(url)
        return self.get(url)
    
    def standardize_date(self, time_data:Any):
        standardized_date = None
        if isinstance(time_data, time.struct_time):
            standardized_date = maya.MayaDT.from_struct(time_data)
        elif isinstance(time_data, str):
            standardized_date = maya.when(time_data)
        elif isinstance(time_data, dateeee.datetime):
            standardized_date = maya.MayaDT.from_datetime(time_data)
        elif isinstance(time_data, float):
            standardized_date = maya.MayaDT(time_data)
        return standardized_date
    
    def _get_date_string(self, _date:maya.MayaDT):
        return f"{_date.year}-{_date.month}-{_date.day}"
    
    def _aggregate_standard(self, _time:Any):
        current_time = self.standardize_date(_time)
        return self._get_date_string(current_time)
    
    def get_intraday(self, ticker, start_date, end_date=time.time()):
        start_date = self._aggregate_standard(start_date)
        end_date = self._aggregate_standard(end_date)
        url = f"iex/{ticker}/prices?startDate={start_date}&endDate={end_date}&resampleFreq={self.freq}&token={self.token}"
        # print(url)
        # self.get(url)
        return {}
    
    def get_daily(self, ticker:str, start_date:Any=(time.time()-(3600 * 280000)), end_date:Any=time.time()):
#         print(start_date)
        start_date = self._aggregate_standard(start_date)
        end_date = self._aggregate_standard(end_date)
        url = f"tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={end_date}&token={self.token}"
        return self.get(url)

if __name__ == "__main__":
    tingo = TiingoAPI("api.tiingo.com")
    tingo['protocol'] = "https"
    tingo.token = "f6deea4df3f704452993854b3d30e3ac4af6560b"
    print(tingo.realtime_ticker("GE"))
