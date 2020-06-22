import re
import time
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

import eft

# --------------------------------------------------------------------------------


def today():
    td = date.today()
    return datetime(year=td.year, month=td.month, day=td.day)


def n_days_from_pivot(pivot_date, n, is_str=False):
    """
    :param n: n为正数时，表示相对于pivot_date之后n天；n为负数时，表示相对于pivot_date之前的-n天
    """
    if is_str:
        pivot_date = str_to_datetime(pivot_date, format="%Y-%m-%d")
    dst = pivot_date + timedelta(days=n)
    if is_str:
        return datetime_to_str(dst, "%Y-%m-%d")
    else:
        return dst


def n_years_ago(datetime, n_years):
    """
    获取datetime往前推n_years的日期
    """
    return datetime - relativedelta(years=n_years)

# --------------------------------------------------------------------------------


def str_to_datetime(str, format="%Y-%m-%d"):
    # string to unaware datetime
    return datetime.strptime(str, format)


def datetime_to_str(datetime, format="%Y-%m-%d"):
    # unaware/aware datetime to string
    return datetime.strftime(format)

# --------------------------------------------------------------------------------


def str_to_date(str, format="%Y-%m-%d"):
    return str_to_datetime(str, format).date()


def date_to_str(date, format="%Y-%m-%d"):
    """
    datetime.date转成字符串
    """
    return date.strftime(format)

# --------------------------------------------------------------------------------


def timestamp_to_datetime(timestamp, timezone):
    div = len(str(timestamp))-10
    timestamp = int(timestamp/(10**div)) # 将13位或16位时间戳转成10位
    utc_dt = datetime.utcfromtimestamp(timestamp)
    aware_utc_dt = utc_dt.replace(tzinfo=eft.UTC_TZ)
    return aware_utc_dt.astimezone(timezone)


def datetime_to_timestamp(dt, bit=10):
    """
    将datetime对象转成时间戳
    :param dt: 可以是带timezone的datetime，这样会自动转成utc；也可以不带timezone，这时会默认按系统时区再转成utc
    :return int
    """
    ts = int(datetime.timestamp(dt))
    ts *= 10**(bit - len(str(ts)))
    return ts

# --------------------------------------------------------------------------------


def str_to_timestamp(str, timezone, format="%Y-%m-%d", bit=10):
    unaware_dt = str_to_datetime(str, format)
    src_dt = timezone.normalize(timezone.localize(unaware_dt)).astimezone(eft.CN_TZ)
    ts = int(time.mktime(src_dt.timetuple())) * (10**(bit-10))
    return ts


def timestamp_to_date(timestamp, timezone):
    """从数据库获取的美股时间戳转换成日期"""
    return timestamp_to_datetime(timestamp, timezone).date()

# --------------------------------------------------------------------------------

def date_str_to_int(date_str):
    """账户资产组将date以int形式存储"""
    return int(re.sub("[^\d]", "", date_str))

# --------------------------------------------------------------------------------
def get_trade_dates(default_trade_dates, start_date=None, end_date=None):
    # 获取某段时间内的交易日
    """
    如果default_trade_dates中元素类型是string, 则start_date和end_date必须是string类型；同理，可以是datetime类型或date类型
    """
    sidx, eidx = None, None
    if start_date:
        if start_date in default_trade_dates:
            sidx = default_trade_dates.index(start_date)
        else:
            # 从start_date往后找最近的交易日
            first_trade_date = trade_date_forward(start_date, default_trade_dates, x=1)
            sidx = default_trade_dates.index(first_trade_date)
    if end_date:
        if end_date in default_trade_dates:
            eidx = default_trade_dates.index(end_date)
        else:
            # 从end_date往前找最近的交易日
            last_trade_date = trade_date_backward(end_date, default_trade_dates, x=1)
            eidx = default_trade_dates.index(last_trade_date)
    if sidx and eidx:
        return default_trade_dates[sidx:eidx + 1]
    elif sidx and not eidx:
        return default_trade_dates[sidx:]
    elif not sidx and eidx:
        return default_trade_dates[:eidx + 1]
    else:
        return default_trade_dates


def trade_date_backward(date, default_trade_dates, x=1):
    # 从date开始往过去推算的第x个交易日, 如果date是交易日, 则返回它前面第x个交易日(计数不包含date); 如果date不是交易日, 同理
    """
    :param date: string, datetime, date
    :param x: int
    :return: string, datetime, date
    """
    assert type(date) == type(default_trade_dates[0]), \
        "date={}和default_trade_dates元素={}的类型应该保持相同".format(
            type(date), type(default_trade_dates[0]))

    # 将str或datetime类型转成date
    if isinstance(date, str):
        date = str_to_date(date, "%Y-%m-%d")
        default_trade_dates = [str_to_date(d, "%Y-%m-%d") for d in get_trade_dates(default_trade_dates)]
    elif isinstance(date, datetime):
        date = date.date()
        default_trade_dates = [d.date() for d in get_trade_dates(default_trade_dates)]

    non_trade_flag = False
    while date not in default_trade_dates:
        non_trade_flag = True
        if date < default_trade_dates[0]:
            return None
        date -= timedelta(days=1)
    idx = default_trade_dates.index(date) - x + int(non_trade_flag)
    if idx < 0:
        return None
    target_date = default_trade_dates[idx]
    if isinstance(date, str):
        target_date = date_to_str(target_date, "%Y-%m-%d")
    elif isinstance(date, datetime):
        target_date = datetime_to_str(target_date, "%Y-%m-%d")
    return target_date


def trade_date_forward(date, default_trade_dates, x=1):
    # 从date开始往未来推算(date包含在内)的第x个交易日
    """
    :param date: string, datetime, date
    :param x: int
    :return: string, datetime, date
    """
    assert type(date) == type(default_trade_dates[0]), \
        "date={}和default_trade_dates元素={}的类型应该保持相同".format(
            type(date), type(default_trade_dates[0]))

    # 将str或datetime类型转成date
    if isinstance(date, str):
        date = str_to_date(date, "%Y-%m-%d")
        default_trade_dates = [str_to_date(d, "%Y-%m-%d") for d in get_trade_dates(default_trade_dates)]
    elif isinstance(date, datetime):
        date = date.date()
        default_trade_dates = [d.date() for d in get_trade_dates(default_trade_dates)]

    non_trade_flag = False
    while date not in default_trade_dates:
        non_trade_flag = True
        date += timedelta(days=1)
        if date > default_trade_dates[-1]:
            return None
    idx = default_trade_dates.index(date) + x - int(non_trade_flag)
    if idx >= len(default_trade_dates):
        return None
    target_date = default_trade_dates[idx]
    if isinstance(date, str):
        target_date = date_to_str(target_date, "%Y-%m-%d")
    elif isinstance(date, datetime):
        target_date = datetime_to_str(target_date, "%Y-%m-%d")
    return target_date

# --------------------------------------------------------------------------------


def start_of_day(trade_date, timezone):
    """
    :param trade_date: datetime.date, 传入的date必须是unaware of timezone的
    :param timezone: pytz timezone
    """
    dt = datetime(trade_date.year, trade_date.month, trade_date.day, 0, 0, 0)
    return timezone.localize(dt)


def start_of_pre_market(trade_date, timezone):
    """
    仅美股有盘前盘后交易
    :param trade_date: datetime.date 交易日期
    :param timezone: pytz timezone
    :return datetime.datetime, 返回当天的盘前交易的开始时刻, 美东4:00am
    """
    dt = datetime(trade_date.year, trade_date.month, trade_date.day, 4, 0, 0)
    return timezone.localize(dt)


def end_of_post_market(trade_date, timezone):
    """返回当天的盘后交易的结束时刻, 美东20:00pm"""
    dt = datetime(trade_date.year, trade_date.month, trade_date.day, 20, 0, 0)
    return timezone.localize(dt)


if __name__ == '__main__':
    from eft.default.timezone import US_EST_TZ, CN_TZ
    a = str_to_timestamp("2020-06-05", timezone=US_EST_TZ)
    print(start_of_pre_market(str_to_datetime("2020-06-10"), US_EST_TZ))
