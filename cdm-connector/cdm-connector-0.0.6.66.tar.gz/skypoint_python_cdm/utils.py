String = str
DateTimeOffset = str
Uri = str
import datetime
import pytz

def getattrIgnoreCase(obj, attr, default=None):
    for i in dir(obj):
        if i.lower() == attr.lower():
            return getattr(obj, attr, default)
    return default


dtype_converter = {
    'int': 'int64',
    'int64' : 'int64',
    'bigint': 'int64',
    'long': 'int64',
    'float64' : 'double',
    'float':'decimal',
    'double': 'double',
    'decimal.Decimal': 'decimal',
    'string': 'string',
    'bool': 'boolean',
    'boolean': 'boolean',
    'datetime': 'dateTime',
    'timestamp': 'dateTime',
}



def to_utc_timestamp(d, format='%Y-%m-%d %H:%M:%S', tz=None):  
    if d is None or d == '':
        return ''  
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime.strptime(d, format)
    if tz:
        tz = pytz.timezone(tz)
        utc_time = tz.normalize(tz.localize(d)).astimezone(pytz.utc)
    else:                    
        try:
            utc_time = d.astimezone(pytz.utc)
        except:
            utc_time = d.tz_localize('UTC')
#   return str(int(utc_time.timestamp()))
    return datetime.datetime.strftime(utc_time, "%Y-%m-%dT%H:%M:%S.%fZ")


def from_utc_timestamp(d, format, tz=None, offset_hour=False):
    if d is None or d == '' or d != d:
        return ''  
    d = str(d)
    if not offset_hour:
        tz = pytz.timezone(tz)
        utc_time = datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.%fZ")
        converted_time = tz.normalize(pytz.utc.localize(utc_time)).astimezone(tz)
    else:
        offset_hour = tz
        hour, minutes = map(int, offset_hour.split(":"))
        if hour < 0:
            days = -1
            total_second = 86400 - (((hour - 2*hour) * 60 + minutes) * 60)
        else:
            days = 0
            total_second = (hour * 60 + minutes) * 60
        converted_time = datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%S.%fZ")
        converted_time = converted_time.replace(tzinfo=datetime.timezone(datetime.timedelta(days=days, seconds=total_second)))
        # converted_time = converted_time + datetime.timedelta(days=days, seconds=total_second)
        # converted_time = datetime.datetime.fromtimestamp(int(d.split(".")[0]), 
        #                     datetime.timezone(datetime.timedelta(days=days, seconds=total_second)))
    return converted_time.strftime(format)