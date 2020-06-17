import datetime
from . import config


def is_holiday(date):
    assert type(date) == str
    return date in config.holiday_list


def is_weekend(date):
    assert type(date) == str
    weekday = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
    return weekday == 5 or weekday == 6


def is_trading_day(date):
    assert type(date) == str
    if is_holiday(date):
        rtn = False
    else:
        if is_weekend(date):
            rtn = False
        else:
            rtn = True
    return rtn


def is_end_of_month(date):
    assert type(date) == str
    import calendar
    year = int(date[0:4])
    month = int(date[5:7])
    day = int(date[8:10])
    end_of_month = calendar.monthrange(year, month)[1]
    return day == end_of_month


def calculate_trading_day(date, date_delta):
    assert type(date_delta) == int
    if date_delta == 0:
        rtn_date = date
    elif date_delta > 0:
        count = 0
        rtn_date = date
        while count < date_delta:
            rtn_date = calculate_calendar_day(rtn_date, 1)
            if is_trading_day(rtn_date):
                count += 1
    else:
        count = 0
        rtn_date = date
        while count > date_delta:
            rtn_date = calculate_calendar_day(rtn_date, -1)
            if is_trading_day(rtn_date):
                count -= 1
    return rtn_date


def calculate_calendar_day(date, date_delta):
    assert type(date) == str
    assert type(date_delta) == int
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    added_date = date_obj + datetime.timedelta(days=date_delta)
    return added_date.strftime("%Y-%m-%d")


def trading_days_between(begin_date, end_date):
    assert type(begin_date) == str
    assert type(end_date) == str
    assert begin_date <= end_date
    trading_day_list = []
    next_day = begin_date
    while next_day <= end_date:
        if is_trading_day(next_day):
            trading_day_list.append(next_day)
        next_day = calculate_calendar_day(next_day, 1)
    return trading_day_list
