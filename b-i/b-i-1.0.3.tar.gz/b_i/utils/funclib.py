#!/usr/bin/env python3
# coding: utf-8

'''
function library, you know .
general function process for data tech.
'''

import datetime

def time_diff(standTime, weeks=0, days=0, hours=0, minutes=0, seconds=0, format="%Y-%m-%d %H:%M:%S"):
    '''
    fromisoformat is only for 3.7+ , dateutil.parser is for 3.6-
    :param standTime: 2019-01-01 or 2019-01-01 01:01 or 2019-01-01 01:01:01 or standTime="now"
    :param weeks: signed integer, eg: 1, -1
    :param days: signed integer, eg: 1, -2
    :param hours: signed integer, eg: 3, -3
    :param minutes: signed integer, eg: 15, -15
    :param seconds: signed integer, eg: 10, -10
    :param format: %Y-%m-%d or %Y-%m-%d %H:%M or %Y-%m-%d %H:%M:%S"
    :return:
    '''
    if standTime == "now":
        stt_pre = datetime.datetime.now()
    else:
        try:
            stt_pre = datetime.datetime.fromisoformat(standTime)
        except:
            import dateutil.parser
            stt_pre = dateutil.parser.parse(standTime)
    stt_next = stt_pre + datetime.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
    return stt_next.strftime(format)


def to_str(parameter):
    '''
    convert any type to str type
    :param parameter:
    :return:
    '''
    if isinstance(parameter, (int, float, bool)) or parameter is None:
        return str(parameter)
    elif isinstance(parameter, str):
        return parameter
    elif isinstance(parameter, list):
        return __list_to_str(parameter)
    elif isinstance(parameter, dict):
        return __dict_to_str(parameter)
    elif isinstance(parameter, tuple):
        return __tuple_to_str(parameter)
    elif isinstance(parameter, set):
        return __set_to_str(parameter)
    elif isinstance(parameter, (datetime.datetime, datetime.date)):
        return __datetime_to_str(parameter)
    else:
        return parameter

def __dict_to_str(data_dict):
    line = '{'
    for k, v in data_dict.items():
        line += '%s: %s, ' % (to_str(k), to_str(v))
    return line.strip(', ') + '}'

def __list_to_str(data_list):
    line = '['
    for var in data_list:
        line += '%s, ' % to_str(var)
    return line.strip(', ') + ']'

def __tuple_to_str(data_tuple):
    return '(' + __list_to_str(list(data_tuple)).strip('[]') + ')'

def __set_to_str(data_set):
    return 'set(' + __list_to_str(list(data_set)) + ')'

def __datetime_to_str(date_time):
    if isinstance(date_time, datetime.date):
        return str(date_time)
    return date_time.strftime('%Y-%m-%d %H:%M:%S %f')


if __name__ == "__main__":
    pass