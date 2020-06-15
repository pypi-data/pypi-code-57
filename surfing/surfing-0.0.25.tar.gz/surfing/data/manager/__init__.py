import datetime
import pandas as pd


class DataManager:

    def __init__(self, start_time, end_time):
        # start_time: None, datetime or '20100101'
        # end_time:   None, datetime or '20100101'
        self.start_time = start_time if isinstance(start_time, datetime.datetime) else datetime.datetime.strptime(start_time,'%Y%m%d')
        self.end_time = end_time if isinstance(end_time, datetime.datetime) else datetime.datetime.strptime(end_time,'%Y%m%d')
        
    def init(self):
        pass

    def terminate(self):
        pass

    @property
    def start_date(self):
        return self.start_time.date()

    @property
    def end_date(self):
        return self.end_time.date()
    
    