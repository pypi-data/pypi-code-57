# -*- coding: utf-8 -*-
import time
from datetime import datetime, date, timedelta

class TimeHelper:
    @staticmethod
    def timestamp_to_strtime(timeStamp):
        """ type timestamp str Convert to type datetime

        :param timeStamp:
        :return: type datetime
        """
        timeArray = time.localtime(timeStamp)
        return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    @staticmethod
    def get_last_time_from_local(format,day):
        return (date.today() + timedelta(days=day)).strftime(format)

    @staticmethod
    def datetime_to_formatstring(time,format):
        if isinstance(time,datetime):
            return time.strftime(format)
    @staticmethod
    def datetime_to_ISO8801(time):
        '''
        将datetime或者timedelta对象转换成ISO 8601时间标准格式字符串
        :param time: 给定datetime或者timedelta
        :return: 根据ISO 8601时间标准格式进行输出
        '''
        if isinstance(time, datetime):  # 如果输入是datetime
            return time.isoformat();
        elif isinstance(time, timedelta):  # 如果输入时timedelta，计算其代表的时分秒
            hours = time.seconds // 3600
            minutes = time.seconds % 3600 // 60
            seconds = time.seconds % 3600 % 60
            return 'P%sDT%sH%sM%sS' % (time.days, hours, minutes, seconds)  # 将字符串进行连接

