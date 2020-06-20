"""Functions to make datetime and timezone manipulation easy, accurate, and reliable."""
import sys
import time
import pytz
import tzlocal
import datetime

def is_naive(the_datetime):
    """Tests if a datetime.datetime object is 'naive', i.e., has no associated timezone information.

        See also is_aware.

    Parameters:
        the_datetime (datetime.datetime) : The datetime to be tested.

    Returns:
        bool : False if the_datetime has timezone information, True if it does not.

    Raises:
        TypeError: Raised if the_datetime parameter is not an instance of datetime.datetime.
    """
    if not isinstance(the_datetime,datetime.datetime):
        raise TypeError("Parameter the_datetime is not an instance of datetime.datetime.")
    if the_datetime.tzinfo is None:
        return True
    else:
        return False

def is_aware(the_datetime):
    """Tests if a datetime.datetime object is 'aware', i.e., has associated timezone information.

        See also is_naive.

    Parameters:
        the_datetime (datetime.datetime) : The datetime to be tested.

    Returns:
        bool : True if the_datetime has timezone information, False if it does not.

    Raises:
        TypeError : Raised if the_datetime parameter is not an instance of datetime.datetime.
    """
    if not isinstance(the_datetime,datetime.datetime):
        raise TypeError("Parameter the_datetime is not an instance of datetime.datetime.")
    if the_datetime.tzinfo is None:
        return False
    else:
        return True

def get_utc_datetime(year,month,day,hour=0,minute=0,second=0,microsecond=0):
    """Returns an aware datetime.datetime object with the specified datetime and associated with UTC timezone.

    Parameters:
        year (int) : The desired year, e.g., 2020.
        month (int) : The desired month number, 1 through 12, e.g., 1 for January and 12 for December.
        day (int) : The desired day of month, e.g., 25.
        hour (int) : The desired hour, 0 through 23, e.g., 14 for 2 p.m.
        minute (int) : The desired minute, 0 through 59, e.g., 33.
        second (int) : The desired second, 0 through 59, e.g., 45. Leap seconds generally ignored.
        microsecond (int) : The desired microsecond, 0 through 999999, e.g., 123456.

    Returns:
        datetime.datetime : An aware datetime.datetime object associated with timezone UTC and with the specified
            date and time values.

    Raises:
        TypeError : Raised if any parameters not of an acceptable type.
        ValueError : Raised if any values outside of valid ranges.
    """
    if not isinstance(year,int):
        raise TypeError("Parameter year is not an int.")
    if not isinstance(month,int):
        raise TypeError("Parameter month is not an int.")
    if not isinstance(day,int):
        raise TypeError("Parameter day is not an int.")
    if not isinstance(hour,int):
        raise TypeError("Parameter hour is not an int.")
    if not isinstance(minute,int):
        raise TypeError("Parameter minute is not an int.")
    if not isinstance(second,int):
        raise TypeError("Parameter second is not an int.")
    if not isinstance(microsecond,int):
        raise TypeError("Parameter microsecond is not an int.")
    tz_utc = pytz.utc
    dt_utc = tz_utc.localize(datetime.datetime(year,month,day,hour,minute,second,microsecond))
    return dt_utc

def get_aware_datetime(year,month,day,hour=0,minute=0,second=0,microsecond=0,timezone=None):
    """Returns an aware datetime.datetime object with the specified datetime and associated timezone.

    Parameters:
        year (int) : The desired year, e.g., 2020.
        month (int) : The desired month number, 1 through 12, e.g., 1 for January and 12 for December.
        day (int) : The desired day of month, e.g., 25.
        hour (int) : The desired hour, 0 through 23, e.g., 14 for 2 p.m.
        minute (int) : The desired minute, 0 through 59, e.g., 33.
        second (int) : The desired second, 0 through 59, e.g., 45. Leap seconds generally ignored.
        microsecond (int) : The desired microsecond, 0 through 999999, e.g., 123456.
        timezone (str or datetime.tzinfo) : Either a valid timezone name as a string, or a timezone object,
            usually a pytz.timezone object which is a child class of datetime.tzinfo.
            If not specified (or None) the default timezone (tzlocal.get_localzone()) is used.

    Returns:
        datetime.datetime : An aware datetime.datetime object associated with timezone UTC and with the specified
            date and time values.

    Raises:
        TypeError : Raised if any parameters not of an acceptable type.
        ValueError : Raised if any values outside of valid ranges.
        pytz.exceptions.UnknownTimeZoneError : Raised is a string timezone name is not recognized.
    """
    if timezone is None:
        timezone = tzlocal.get_localzone()
    if not isinstance(year,int):
        raise TypeError("Parameter year is not an int.")
    if not isinstance(month,int):
        raise TypeError("Parameter month is not an int.")
    if not isinstance(day,int):
        raise TypeError("Parameter day is not an int.")
    if not isinstance(hour,int):
        raise TypeError("Parameter hour is not an int.")
    if not isinstance(minute,int):
        raise TypeError("Parameter minute is not an int.")
    if not isinstance(second,int):
        raise TypeError("Parameter second is not an int.")
    if not isinstance(microsecond,int):
        raise TypeError("Parameter microsecond is not an int.")
    if timezone.__class__.__name__ == "str":
        timezone = pytz.timezone(timezone)
    elif not isinstance(timezone,datetime.tzinfo):
        raise TypeError("Parameter timezone is not a timezone name or an instance of datetime.tzinfo.")
    aware_dt = timezone.localize(datetime.datetime(year,month,day,hour,minute,second,microsecond))
    return aware_dt

def get_epoch_from_aware_datetime(aware_datetime):
    """Returns number of seconds (including fractions) from the epoch base instant to aware_datetime instant.

    Parameters:
        aware_datetime (datetime.datetime) : A timezone aware datetime.datetime object.

    Returns:
        datetime.datetime : An aware datetime.datetime object associated with timezone UTC and with the
            specified date and time values.

    Raises:
        TypeError : Raised if any parameters not of an acceptable type.
        RunTimeError : Raised if paraneter aware_datetime is naive, not aware.
    """
    if is_naive(aware_datetime):
        raise RuntimeError("Datetime parameter is not timezone aware.")
    base_epoch = datetime.datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    dt_epoch = (aware_datetime - base_epoch).total_seconds()   # fractional seconds
    return dt_epoch

def get_utc_datetime_from_epoch(epoch=None):
    """Returns a UTC timezone aware datetime.datetime set from the epoch seconds (including fractions).

    Parameters:
        epoch (float) : Number of seconds (including fractions) since system epoch. Can also be an int.
            If not specified (None) then time.time(), the current system time epoch, is used.

    Returns:
        datetime.datetime : An aware datetime.datetime object associated with timezone UTC and with the
            equivalent date and time values.

    Raises:
        TypeError : Raised if any parameters not of an acceptable type.
    """
    if epoch is None:
        epoch = time.time()
    if not isinstance(epoch,int) and not isinstance(epoch,float):
        raise TypeError("Epoch parameter is not an int or a float.")
    aware_dt = datetime.datetime.fromtimestamp(epoch,pytz.utc)
    return aware_dt

def get_aware_datetime_from_epoch(epoch=None,timezone=None):
    """Returns a datetime.datetime set from the epoch seconds and aware of specified timezone.

    Parameters:
        epoch (float) : Number of seconds (including fractions) since system epoch. Can also be an int.
            If not specified (or None) the current system epoch (time.time()) is used.
        timezone (str or datetime.tzinfo) : Either a valid timezone name as a string, or a timezone object,
            usually a pytz.timezone object, which is a subclass of datetime.tzinfo.
            If not specified (or None) the default timezone (tzlocal.get_localzone()) is used.

    Returns:
        datetime.datetime : An aware datetime.datetime object associated with specified timezone and with the
            equivalent datetime values.

    Raises:
        TypeError : Raised if any parameters not of an acceptable type.
    """
    if epoch is None:
        epoch = time.time()
    if timezone is None:
        timezone = tzlocal.get_localzone()
    if not isinstance(epoch,int) and not isinstance(epoch,float):
        raise RuntimeError("Epoch parameter is an int or a float.")
    if timezone.__class__.__name__ == "str":
        timezone = pytz.timezone(timezone)
    elif not isinstance(timezone,datetime.tzinfo):
        raise TypeError("Parameter timezone is not a timezone name or an instance of datetime.tzinfo.")
    aware_dt = datetime.datetime.fromtimestamp(epoch,timezone)
    return aware_dt

def get_aware_datetime_from_naive(naive_datetime,timezone=None):
    """Returns a localized (made timezone aware) datetime.datetime but does not convert any date or time values.

    Parameters:
        naive_datetime (datetime.datetime) : A naive datetime.datetime object (not internally associated with
            any timezone).
        timezone (str or datetime.tzinfo) : Either a valid timezone name as a string, or a timezone object,
            usually a pytz.timezone object, which is a subclass of datetime.tzinfo.
            If not specified (or None) the default timezone (tzlocal.get_localzone()) is used.

    Returns:
        datetime.datetime : A datetime.datetime object aware of a specific timezone.

    Raises:
        TypeError : Raised if any parameters not of an acceptable type.
        RunTimeError : Raised if naive_datetime parameter not naive but is rather timezone aware.
    """
    if timezone is None:
        timezone = tzlocal.get_localzone()
    # Localized naive datetime, but no timezone conversion performed.
    if is_aware(naive_datetime):
        raise RuntimeError("Naive datetime parameter is not naive.")
    if timezone.__class__.__name__ == "str":
        timezone = pytz.timezone(timezone)
    elif not isinstance(timezone,datetime.tzinfo):
        raise TypeError("Parameter timezone is not a timezone name or an instance of datetime.tzinfo.")
    aware_dt = timezone.localize(naive_datetime)
    return aware_dt

def get_now_aware_datetime(timezone=None):
    """Returns a timezone aware datetime of the current date and time in the specified timezone.

    Parameters:
        timezone (str or datetime.tzinfo) : Either a valid timezone name as a string, or a timezone object,
            usually a pytz.timezone object, which is a subclass of datetime.tzinfo.
            If not specified (or None) the default timezone (tzlocal.get_localzone()) is used.

    Returns:
        datetime.datetime : A datetime.datetime object with current datetime in the specified timezone.

    Raises:
        TypeError : Raised if any parameters not of an acceptable type.
    """
    if timezone is None:
        timezone = tzlocal.get_localzone()
    if timezone.__class__.__name__ == "str":
        timezone = pytz.timezone(timezone)
    elif not isinstance(timezone,datetime.tzinfo):
        raise TypeError("Parameter timezone is not a timezone name or an instance of datetime.tzinfo.")
    epoch = time.time()
    aware_dt = datetime.datetime.fromtimestamp(epoch,timezone)
    return aware_dt

def convert_aware_datetime(old_aware_datetime,timezone=None):
    """Converts a timezone aware datetime into another datetime aware of another timezone.

    Parameters:
        old_aware_datetime (datetime.datetime) : A timezone aware datetime.
        timezone (str or datetime.tzinfo) : Either a valid timezone name as a string, or a timezone object,
            usually a pytz.timezone object, which is a subclass of datetime.tzinfo.
            If not specified (or None) the default timezone (tzlocal.get_localzone()) is used.

    Returns:
        datetime.datetime : A datetime.datetime object aware of the new timezone and with properly converted
            date and time values.

    Raises:
        RunTimeError : Raised if old_aware_datetime parameter is not aware of any timezone.
        TypeError : Raised if any parameters not of an acceptable type.
    """
    if timezone is None:
        timezone = tzlocal.get_localzone()
    if is_naive(old_aware_datetime):
        raise RuntimeError("Datetime parameter is not timezone aware.")
    if timezone.__class__.__name__ == "str":
        timezone = pytz.timezone(timezone)
    elif not isinstance(timezone,datetime.tzinfo):
        raise TypeError("Parameter timezone is not a timezone name or an instance of datetime.tzinfo.")
    new_aware_datetime = old_aware_datetime.astimezone(timezone)
    return new_aware_datetime

def get_naive_datetime(old_aware_datetime):
    """Converts a timezone aware datetime into a naive datetime with same date and time values.

    Parameters:
        old_aware_datetime (datetime.datetime) : Preferably a timezone aware datetime, but might
            redundantly also be a naive datetime.

    Returns:
        datetime.datetime : A datetime.datetime object not aware (naive) of any timezone and with the same
            date and time values.

    Raises:
        TypeError : Raised if any parameters not of an acceptable type.
    """
    if not isinstance(old_aware_datetime,datetime.datetime):
        raise TypeError("Parameter old_aware_datetime is not an instance of datetime.datetime.")
    new_naive_datetime = old_aware_datetime.replace(tzinfo=None)
    return new_naive_datetime

def format_datetime(the_datetime, datefmt='%Y-%m-%d %H:%M:%S.%f %Z%z', precision=6, nanoseconds=None):
    """Formats datetime.datetime objects like strftime method but with flexible precision and even nanoseconds.

    Parameters:
        the_datetime (datetime.datetime) : A datetime.datetime object.
        datefmt (str) : A strftime compatible date format.
        precision (int) : Desired decimal digit preceision of fractional seconds.
        nanoseconds (int) : Number of nanoseconds to associate with the datatime object. This is not needed if
            the built-in microsecond precision (precision=6) of datetime is sufficient, but if greater
            precision is desired (up to nanosecond) this parameter must be specified.

    Returns:
        str : A formatter date and time.

    Raises:
        TypeError : Raised if any parameters not of an acceptable type.
    """
    if not isinstance(the_datetime,datetime.datetime):
        raise TypeError("Parameter the_datetime is not an instance of datetime.datetime.")
    precision = min(9,max(0,int(precision)))
    microseconds = the_datetime.microsecond
    if microseconds is None:
        microseconds = 0
    if nanoseconds is None:
        nanoseconds = microseconds * 1000  # use nanoseconds by extending datetime microseconds
    if datefmt.find('%f') >= 0:
        digits = '%09d' % nanoseconds # format with leading zeros
        digits = digits[0:precision]
        datefmt = datefmt.replace('%f', digits)
    formatted_datetime = the_datetime.strftime(datefmt)
    return formatted_datetime
