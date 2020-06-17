import string
import datetime
import re
from ... import calendar


def is_futures(instrument_id: str):
    pattern = '^([a-z]{1,2}|[A-Z]{1,2})[0-9]{3,4}$'
    res = re.match(pattern, instrument_id)
    if res:
        return True
    else:
        return False


def get_delivery_year_and_month(date, instrument_id):
    assert len(date) == 10
    assert is_futures(instrument_id)
    digit_part = get_digit_part(instrument_id)
    if len(digit_part) == 4:
        yy = digit_part[0:2]
        for i in range(20):
            year = str(int(date[0:4]) + i)
            if year[2:4] == yy:
                return int(year), int(digit_part[-2:])
    elif len(digit_part) == 3:
        y = digit_part[0:1]
        for i in range(20):
            year = str(int(date[0:4]) + i)
            if year[3:4] == y:
                return int(year), int(digit_part[-2:])
    else:
        raise Exception(f'get_delivery_year_and_month({date}, {instrument_id})')

    raise Exception(f'get_delivery_year_and_month({date}, {instrument_id})')


def get_equal_latter_instrument(date_1, date_2, instrument_id_1, instrument_id_2):
    year1, month1 = get_delivery_year_and_month(date_1, instrument_id_1)
    year2, month2 = get_delivery_year_and_month(date_2, instrument_id_2)
    yyyymm1 = year1 * 100 + month1
    yyyymm2 = year2 * 100 + month2
    if yyyymm1 >= yyyymm2:
        return instrument_id_1
    else:
        return instrument_id_2


def get_equal_earlier_instrument(date_1, date_2, instrument_id_1, instrument_id_2):
    year1, month1 = get_delivery_year_and_month(date_1, instrument_id_1)
    year2, month2 = get_delivery_year_and_month(date_2, instrument_id_2)
    yyyymm1 = year1 * 100 + month1
    yyyymm2 = year2 * 100 + month2
    if yyyymm1 <= yyyymm2:
        return instrument_id_1
    else:
        return instrument_id_2


def get_friday_of_month_by_count(year, month, count):
    assert 1000 < year < 2500
    assert 1 <= month <= 12
    assert 1 <= count <= 5
    first_date = datetime.date(year, month, 1)
    weekday_of_first_date = first_date.timetuple().tm_wday
    if weekday_of_first_date <= 4:
        diff = (count - 1) * 7 + 4 - weekday_of_first_date
        target_day = first_date + datetime.timedelta(days=diff)
    else:
        diff = count * 7 + 4 - weekday_of_first_date
        target_day = first_date + datetime.timedelta(days=diff)
    if target_day.month != month and target_day.year != year:
        raise Exception(f'invalid count({count})')
    return target_day.strftime('%Y-%m-%d')


def get_trading_day_of_month_by_count(year, month, count):
    assert 1000 < year < 2500
    assert 1 <= month <= 12
    assert count != 0
    n = 0
    if count > 0:
        first_date = datetime.date(year, month, 1)
        for i in range(31):
            rtn_date = first_date + datetime.timedelta(days=i)
            if calendar.is_trading_day(rtn_date.strftime('%Y-%m-%d')):
                n += 1
            if n == count:
                if rtn_date.month != month and rtn_date.year != year:
                    raise Exception(f'invalid count({count})')
                return rtn_date.strftime('%Y-%m-%d')
    else:
        next_year, next_month = get_next_month(year, month)
        first_date = datetime.date(next_year, next_month, 1)
        for i in range(31):
            rtn_date = first_date - datetime.timedelta(days=i + 1)
            if calendar.is_trading_day(rtn_date.strftime('%Y-%m-%d')):
                n -= 1
            if n == count:
                if rtn_date.month != month and rtn_date.year != year:
                    raise Exception(f'invalid count({count})')
                return rtn_date.strftime('%Y-%m-%d')


def get_calendar_day_of_month_by_count(year, month, count):
    assert 1000 < year < 2500
    assert 1 <= month <= 12
    assert count != 0
    if count > 0:
        first_date = datetime.date(year, month, 1)
        rtn_date = first_date + datetime.timedelta(days=count - 1)
    else:
        next_year, next_month = get_next_month(year, month)
        first_date = datetime.date(next_year, next_month, 1)
        rtn_date = first_date + datetime.timedelta(days=count)
    if rtn_date.month != month and rtn_date.year != year:
        raise Exception(f'invalid count({count})')
    return rtn_date.strftime('%Y-%m-%d')


def get_next_month(year, month):
    month_num = year * 12 + month + 1
    assert 1 <= month <= 12
    _year = int((month_num - 1) / 12)
    _month = month_num - year * 12
    _month = _month if _month <= 12 else 1
    return _year, _month


def get_prev_month(year, month):
    assert 1000 < year < 2500
    assert 1 <= month <= 12
    month_num = year * 12 + month - 1
    _year = int((month_num - 1) / 12)
    _month = month_num - year * 12
    _month = _month if _month > 0 else 12
    return _year, _month


def get_letter_part(in_str):
    pattern = string.ascii_letters
    rtn_str = ''
    for char in in_str:
        if char in pattern:
            rtn_str += char
    return rtn_str


def get_digit_part(in_str):
    rtn_str = ''
    for char in in_str:
        if char.isdigit():
            rtn_str += char
    return rtn_str


def parse_last_trading_day(date: str, instrument_id: str, last_td_rule: str):
    year, month = get_delivery_year_and_month(date, instrument_id)
    rule = last_td_rule.split('_')
    if 'PREMONTH' in rule:
        year, month = get_prev_month(year, month)
        rule.remove('PREMONTH')
    count = int(rule[0][:-2])
    if rule[1] == 'CD':
        rtn_date = get_calendar_day_of_month_by_count(year, month, count)
        if calendar.is_trading_day(rtn_date):
            return rtn_date
        else:
            return calendar.calculate_trading_day(rtn_date, 1)
    elif rule[1] == 'TD':
        return get_trading_day_of_month_by_count(year, month, count)
    elif rule[1] == 'FRI':
        rtn_date = get_friday_of_month_by_count(year, month, count)
        if calendar.is_trading_day(rtn_date):
            return rtn_date
        else:
            return calendar.calculate_trading_day(rtn_date, 1)
    else:
        raise Exception('invalid rule')


def parse_time_line(time_info, date, cycle):
    # '21:00:00-23:30:00+09:00:00-10:15:00+10:30:00-11:30:00+13:30:00-15:00:00'
    prev_trading_date = calendar.calculate_trading_day(date, -1)
    next_calendar_day_of_pre_trading_day = calendar.calculate_calendar_day(prev_trading_date, 1)
    time_list = time_info.split('+')
    time_profile = []
    for item in time_list:
        split_time = item.split('-')
        begin_time = split_time[0]
        end_time = split_time[1]
        # check is night
        if begin_time > '17:00:00':
            begin_datetime = '{0} {1}'.format(prev_trading_date, begin_time)
            # check is next calendar day
            if end_time < begin_time:
                end_datetime = '{0} {1}'.format(next_calendar_day_of_pre_trading_day, end_time)
            else:
                end_datetime = '{0} {1}'.format(prev_trading_date, end_time)
        else:
            begin_datetime = '{0} {1}'.format(date, begin_time)
            end_datetime = '{0} {1}'.format(date, end_time)
        time_profile.append([begin_datetime, end_datetime])
    time_line = []
    for period in time_profile:
        current_time = datetime.datetime.strptime(period[0], "%Y-%m-%d %H:%M:%S")
        current_time += datetime.timedelta(minutes=cycle)
        end_time = datetime.datetime.strptime(period[1], "%Y-%m-%d %H:%M:%S")
        while current_time <= end_time:
            time_line.append(current_time.strftime("%Y-%m-%d %H:%M:%S"))
            current_time += datetime.timedelta(minutes=cycle)
    return time_line


def parse_std_instrument_id(date, raw_instrument_id):
    delivery_year, delivery_month = get_delivery_year_and_month(date, raw_instrument_id)
    if raw_instrument_id[-4].isdigit():
        std_instrument_id = raw_instrument_id.upper()
        return std_instrument_id
    else:
        str_delivery_year = str(delivery_year)
        std_instrument_id = raw_instrument_id[:-3] + str_delivery_year[2] + raw_instrument_id[-3:]
        std_instrument_id = std_instrument_id.upper()
        return std_instrument_id
