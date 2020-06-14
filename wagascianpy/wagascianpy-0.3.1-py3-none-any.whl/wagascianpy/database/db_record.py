#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020 Pintaudi Giorgio
#

""" Virtual database record class """

import abc
from datetime import datetime

import pytz
from enum import IntEnum, Enum

# compatible with Python 2 *and* 3:
ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})

_DEFAULT_TIMEZONE = "Asia/Tokyo"


###########################################################################
#                                DBRecord                                 #
###########################################################################

class DBRecord(ABC):
    """Generic database record record"""

    _timezone = _DEFAULT_TIMEZONE

    def __init__(self, record=None):

        if record is not None:
            for init_member, init_value in record.items():
                if init_member in self.list_fields():
                    setattr(self, init_member, init_value)

    def is_ready(self):
        """Return True if the make_record method is ready to be called on the object"""
        for member in dir(self):
            value = getattr(self, member)
            if not member.startswith('_') and not callable(value):
                if value is None:
                    print(member)
                    return False
        return True

    def set_timezone(self, timezone):
        """ Change the timezone (default timezone is Asia/Tokyo)"""
        self._timezone = timezone

    def make_record(self):
        """Return a dictionary containing the full record"""
        record = {}
        for member in dir(self):
            value = getattr(self, member)
            if not member.startswith('_') and not callable(value):
                if value is None:
                    raise ValueError("Field %s is not set" % member)
                elif isinstance(value, float):
                    record[member] = float(value)
                elif isinstance(value, (int, Enum, IntEnum)):
                    record[member] = int(value)
                else:
                    record[member] = str(value)
        return record

    def list_fields(self):
        """List all the field names of the record"""
        return list(
            filter(lambda member: not member.startswith('__') and not callable(getattr(self, member)), dir(self)))

    @classmethod
    def datetime2timestamp(cls, datetime_arg):
        """Convert from datetime string to timestamp
        """
        if isinstance(datetime_arg, datetime):
            try:
                try:
                    timestamp = pytz.timezone(DBRecord._timezone).localize(datetime_arg).timestamp()
                except ValueError:
                    timestamp = datetime_arg.timestamp()
            except AttributeError:
                unix_origin = datetime(1970, 1, 1, tzinfo=pytz.utc)
                try:
                    timestamp = (pytz.timezone(DBRecord._timezone).localize(datetime_arg) - unix_origin).total_seconds()
                except ValueError:
                    timestamp = (datetime_arg - unix_origin).total_seconds()
            return float(timestamp)
        elif isinstance(datetime_arg, str):
            return cls.str2timestamp(datetime_arg)
        elif isinstance(datetime_arg, int) or isinstance(datetime_arg, float):
            return float(datetime_arg)
        else:
            raise ValueError("Datetime argument not recognized %s" % datetime_arg)

    @classmethod
    def timestamp2datetime(cls, posix_timestamp):
        """Convert from timestamp to datetime
        """
        utc_dt = datetime.utcfromtimestamp(posix_timestamp).replace(tzinfo=pytz.utc)
        return utc_dt.astimezone(pytz.timezone(DBRecord._timezone))

    @classmethod
    def add_timezone(cls, datetime_arg):
        """Add timezone info to datetime
        """
        if datetime_arg.tzinfo is not None and datetime_arg.tzinfo.utcoffset(datetime_arg) is not None:
            return datetime_arg
        else:
            return datetime_arg.astimezone(pytz.timezone(DBRecord._timezone))

    @classmethod
    def timestamp2str(cls, posix_timestamp):
        """Convert from timestamp to human readable date string
        """
        return cls.timestamp2datetime(posix_timestamp).strftime('%Y/%m/%d %H:%M:%S %Z')

    @classmethod
    def str2timestamp(cls, string):
        """Convert from human readable date string to timestamp
        """
        return cls.datetime2timestamp(cls.str2datetime(string))

    @classmethod
    def str2datetime(cls, string):
        try:
            time = pytz.timezone(DBRecord._timezone).localize(datetime.strptime(string, "%Y/%m/%d %H:%M:%S"))
        except ValueError:
            time = pytz.timezone(DBRecord._timezone).localize(datetime.strptime(string, "%Y/%m/%d %H:%M:%S %Z"))
        return time

    @classmethod
    def get_timezone_str(cls):
        return cls._timezone

    def pretty_print(self):
        """Print the run record to standard output"""
        for member in dir(self):
            value = getattr(self, member)
            if not member.startswith('__') and not callable(value):
                print("%s : %s" % (member, str(value)))
