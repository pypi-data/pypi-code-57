from distutils.util import strtobool
from datetime import datetime, date, time
try:
    from fastnumbers import fast_float as float, fast_int as int
except ImportError:
    pass

str2int = int
str2float = float
str2pct = lambda val: float(val.replace('%', '')) / 100.0
str2date = lambda val: date(*map(int, sep_date(val)))
str2time = lambda val: time(*map(int, val.split(':')))

def str2bool(val):
    try:
        if val == u'\u662f' or strtobool(val) == 1:
            return True
    except ValueError:
        pass
    return False

def sep_date(val):
    for symbol in ('-', '/', '.', '\\'):
        if symbol in val:
            return val.split('-')
    assert len(val) == 8, 'cannot transfer "%s" into a date' % symbol
    return val[:4], val[4:6], val[6:]

def str2dt(val):
    day, time = val.split(' ', 1)
    _day = tuple(map(int, sep_date(day)))
    if time.endswith('PM'):
        hasPM = True
    time = time.replace('PM', '').replace('AM', '')
    _time = list(map(int, time.split(':')))
    if hasPM:
        _time[0] += 12
    if len(_time) != 3:
        _time.append(0)
    return datetime(_day[0], _day[1], _day[2], _time[0], _time[1], _time[2])
