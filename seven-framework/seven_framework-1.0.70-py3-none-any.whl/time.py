'''
@Author: ChenXiaolei
@Date: 2020-03-06 23:17:54
@LastEditTime: 2020-03-21 16:50:31
@LastEditors: ChenXiaolei
@Description: time helper
@FilePath: /python_base_framework/libs./seven_framework/time.py
'''
# -*- coding: utf-8 -*-

import time
import datetime
from dateutil.relativedelta import relativedelta


class TimeHelper:
    @classmethod
    def format_time_to_datetime(self,
                                format_time=None,
                                format='%Y-%m-%d %H:%M:%S'):
        """
        @description: 时间字符串转datetime
        @param format_time: 格式化时间，如果未传则取服务器当前时间
        @param format: 格式化时间格式
        @return: datetime
        @last_editors: ChenXiaolei
        """
        if not format_time:
            return datetime.datetime.now()
        return datetime.datetime.strptime(format_time, format)

    @classmethod
    def datetime_to_format_time(self, dt, format='%Y-%m-%d %H:%M:%S'):
        """
        @description: datetime转时间字符串
        @param dt: datetime格式时间
        @param format: 格式化时间格式
        @return: 时间字符串
        @last_editors: ChenXiaolei
        """
        return dt.strftime(format)

    @classmethod
    def datetime_to_timestamp(self,
                              dt,
                              format='%Y-%m-%d %H:%M:%S',
                              out_ms=False):
        """
        @description: datetime转unix时间戳
        @param dt: datetime格式时间
        @param format: 格式化时间格式
        @return: unix时间戳
        @last_editors: ChenXiaolei
        """
        if out_ms:
            return int(
                time.mktime(dt.timetuple()) * 1000.0 + dt.microsecond / 1000.0)
        return int(time.mktime(dt.timetuple()))

    @classmethod
    def format_time_to_timestamp(self,
                                 format_time=None,
                                 format='%Y-%m-%d %H:%M:%S'):
        """
        @description: 格式化时间转为Unix时间戳
        @param format_time: 格式化时间，如果未传则返回服务器当前时间
        @param format: 格式化时间格式
        @return: Unix时间戳
        @last_editors: ChenXiaolei
        """
        if format_time:
            time_tuple = time.strptime(format_time, format)
            result = time.mktime(time_tuple)
            return int(result)
        return int(time.time())

    @classmethod
    def timestamp_to_format_time(self,
                                 timestamp=None,
                                 format='%Y-%m-%d %H:%M:%S'):
        """
        @description: 时间戳转格式化时间
        @param timestamp: unix时间戳 
        @param format: 格式化时间格式
        @return: datetime
        @last_editors: ChenXiaolei
        """
        if timestamp:
            time_tuple = time.localtime(timestamp)
            result = time.strftime(format, time_tuple)
            return result
        else:
            return time.strftime(format)

    @classmethod
    def timestamp_to_datetime(self, timestamp=time.time()):
        """
        @description: unix时间戳转datetime
        @param timestamp: unix时间戳，如果没传默认取服务器当前时间
        @return: datetime
        @last_editors: ChenXiaolei
        """
        if self.is_ms_timestamp(timestamp):
            timestamp = timestamp / 1000
        return datetime.datetime.fromtimestamp(timestamp)

    @classmethod
    def get_now_timestamp(self):
        """
        @description: 获取当前时间戳
        @return: 时间戳
        @last_editors: ChenXiaolei
        """
        return int(time.time())

    # 获取当前时间格式
    @classmethod
    def get_now_datetime(self):
        """
        @description: 获取当前时间格式
        @return: 格式化时间
        @last_editors: ChenXiaolei
        """
        return datetime.datetime.now()

    @classmethod
    def get_now_format_time(self, format='%Y-%m-%d %H:%M:%S'):
        """
        @description: 获取当前时间格式
        @param format: 格式化时间格式
        @return: datetime
        @last_editors: ChenXiaolei
        """
        return datetime.datetime.now().strftime(format)

    @classmethod
    def is_ms_timestamp(self, timestamp):
        """
        @description: 时间戳是否为毫秒时间戳
        @param timestamp: unix时间戳 
        @return: bool
        @last_editors: ChenXiaolei
        """
        if timestamp and len(str(int(timestamp))) > 10:
            return True
        else:
            return False

    @classmethod
    def add_seconds_by_timestamp(self, timestamp=None, second=1):
        """
        @description: 为时间戳增加秒数
        @param timestamp: unix时间戳 
        @param second: 秒数
        @return: unix时间戳
        @last_editors: ChenXiaolei
        """
        if not timestamp:
            timestamp = self.get_now_timestamp()

        # 毫秒时间戳
        if self.is_ms_timestamp(timestamp):
            return timestamp + (second * 1000)
        else:
            return timestamp + second

    @classmethod
    def add_minutes_by_timestamp(self, timestamp=None, minute=1):
        """
        @description: 为时间戳增加分钟数
        @param timestamp: unix时间戳 
        @param minute: 分钟数
        @return: unix时间戳
        @last_editors: ChenXiaolei
        """
        return self.add_seconds_by_timestamp(timestamp, minute * 60)

    @classmethod
    def add_hours_by_timestamp(self, timestamp=None, hour=1):
        """
        @description: 为时间戳增加小时数
        @param timestamp: unix时间戳 
        @param hour: 小时数
        @return: unix时间戳
        @last_editors: ChenXiaolei
        """
        return self.add_seconds_by_timestamp(timestamp, hour * 3600)

    @classmethod
    def add_days_by_timestamp(self, timestamp=None, day=1):
        """
        @description: 为时间戳增加天数
        @param timestamp: unix时间戳 
        @param day: 天数
        @return: unix时间戳
        @last_editors: ChenXiaolei
        """
        return self.add_seconds_by_timestamp(timestamp, day * 86400)

    @classmethod
    def add_months_by_timestamp(self, timestamp=None, months=1):
        """
        @description: 为时间戳增加月数
        @param timestamp: unix时间戳 
        @param months: 月数
        @return: unix时间戳
        @last_editors: ChenXiaolei
        """
        if not timestamp:
            timestamp = time.time()

        dt = self.timestamp_to_datetime(timestamp)
        return self.datetime_to_timestamp(
            dt + relativedelta(months=months),
            out_ms=self.is_ms_timestamp(timestamp))

    @classmethod
    def add_years_by_timestamp(self, timestamp=None, years=1):
        """
        @description: 为时间戳增加年数
        @param timestamp: unix时间戳 
        @param years: 年数
        @return: unix时间戳
        @last_editors: ChenXiaolei
        """
        if not timestamp:
            timestamp = time.time()

        dt = self.timestamp_to_datetime(timestamp)
        return self.datetime_to_timestamp(
            dt + relativedelta(years=years),
            out_ms=self.is_ms_timestamp(timestamp))

    @classmethod
    def add_second_by_format_time(self,
                                  format_time=None,
                                  second=1,
                                  format='%Y-%m-%d %H:%M:%S'):
        """
        @description: 为时间格式增加秒数
        @param format_time: 格式化时间，如果未传则取服务器当前时间
        @param second: 秒数 
        @return: datetime
        @last_editors: ChenXiaolei
        """
        return (self.format_time_to_datetime(format_time, format) +
                datetime.timedelta(seconds=second)).strftime(format)

    @classmethod
    def add_minutes_by_format_time(self,
                                   format_time=None,
                                   minute=1,
                                   format='%Y-%m-%d %H:%M:%S'):
        """
        @description: 为时间格式增加分钟数
        @param format_time: 格式化时间，如果未传则取服务器当前时间
        @param minute: 分钟数
        @param format: 格式化时间格式
        @return: datetime
        @last_editors: ChenXiaolei
        """
        return (self.format_time_to_datetime(format_time, format) +
                datetime.timedelta(minutes=minute)).strftime(format)

    @classmethod
    def add_hours_by_format_time(self,
                                 format_time=None,
                                 hour=1,
                                 format='%Y-%m-%d %H:%M:%S'):
        """
        @description: 为时间格式增加小时数
        @param format_time: 格式化时间，如果未传则取服务器当前时间
        @param hour: 小时数
        @param format: 格式化时间格式
        @return: datetime
        @last_editors: ChenXiaolei
        """
        return (self.format_time_to_datetime(format_time, format) +
                datetime.timedelta(hours=hour)).strftime(format)

    @classmethod
    def add_days_by_format_time(self,
                                format_time=None,
                                day=1,
                                format='%Y-%m-%d %H:%M:%S'):
        """
        @description: 为时间格式增加分钟数
        @param format_time: 格式化时间，如果未传则取服务器当前时间
        @param day: 天数
        @param format: 格式化时间格式
        @return: datetime
        @last_editors: ChenXiaolei
        """
        return (self.format_time_to_datetime(format_time, format) +
                datetime.timedelta(days=day)).strftime(format)

    @classmethod
    def add_months_by_format_time(self,
                                  format_time=None,
                                  months=1,
                                  format='%Y-%m-%d %H:%M:%S'):
        """
        @description: 为时间格式增加月数
        @param format_time: 格式化时间，如果未传则取服务器当前时间
        @param months: 月数
        @param format: 格式化时间格式
        @return: datetime
        @last_editors: ChenXiaolei
        """
        return (self.format_time_to_datetime(format_time, format) +
                relativedelta(months=months)).strftime(format)

    @classmethod
    def add_years_by_format_time(self,
                                 format_time=None,
                                 years=1,
                                 format='%Y-%m-%d %H:%M:%S'):
        """
        @description: 为时间格式增加年数
        @param format_time: 格式化时间，如果未传则取服务器当前时间
        @param years: 年数
        @param format: 格式化时间格式
        @return: datetime
        @last_editors: ChenXiaolei
        """
        return (self.format_time_to_datetime(format_time, format) +
                relativedelta(years=years)).strftime(format)
