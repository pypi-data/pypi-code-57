# general utilities
import os
from itertools import chain
from termcolor import colored
import datetime
import pytz
import random
import subprocess
import copy

######## FILE IO ########

def read_file(fpath):
  try:
    f = open(fpath, 'r')
    s = f.read()
    f.close()
    return s
  except Exception as e:
    # error message?
    return None

def write_file(fnom, s):
  f = open(fnom, 'w')
  f.write(s)
  f.close()

# most of the time you're gonna want to add '\n' to s
def append_file(fnom, s):
  f = open(fnom, 'a')
  f.write(s)
  f.close()


######### DATE SHIT #########

def str_to_date(date_str):
  return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

def date_to_str(dat):
  return dat.strftime('%Y-%m-%d')

def unixtime_to_str(t):
  return datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def unixtime_to_str_in_timezone(t, tz_str):
  return datetime.datetime.utcfromtimestamp(t).replace(tzinfo=pytz.timezone('utc')).astimezone(pytz.timezone(tz_str)).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def str_to_datetime_in_timezone(day_str, time_str, tz_str):
  tmp_time_obj = datetime.datetime.strptime(
      '%s %s' % (day_str, time_str), '%Y-%m-%d %H:%M:%S')
  return pytz.timezone(tz_str).localize(tmp_time_obj)


############ MISC ############

def coalesce(a, b):
  if a is None:
    return b
  return a

def identity(x):
  return x