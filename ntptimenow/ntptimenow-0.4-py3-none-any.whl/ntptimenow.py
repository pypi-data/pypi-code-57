# -*- coding: utf-8 -*-
from datetime import datetime
from ntplib import NTPClient

class NTPTimeNow:
    def __init__(self,poolservers:str='time.kku.ac.th',version:int=3):
        """
        Python NTP Time Now

        :param str poolservers: poolservers is NTP server. (default is time.kku.ac.th)
        :param int version: version of NTP server. (default is 3)
        """
        self.version = version
        self.poolservers = poolservers

    def ntp_now(self)->datetime:
        """
        NTP time now

        :return: datetime from NTP server.
        :rtype: datetime.datetime
        """
        response = NTPClient().request(self.poolservers,version=self.version)
        return datetime.fromtimestamp(response.tx_time)