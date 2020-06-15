"""
Copyright 2020 zGlue, Inc.

Licensed under zOH License version 1.0 ("the license") that is included in the accompanying repository.  
You may not use this file except in compliance with the License. 
You may obtain a copy of the license at <https://zglue.com/oci/zohl1v>.

Utility functions for printing & testing
"""

import time
import inspect
import statistics as stat
from functools import wraps


SUCCESS = 0
FAIL = -1

PERFORMANCE_DATA = {}
FT_CLKDIV_LIST = [ round( (60.0E6 / ((1 + i)*2)) , 1) for i in range(0, 0xffff)]

IS_CLI_CMD = "isCliCmd"
OPEN_HOST_ATTR = "openHost"


def log_performance(func):

    @wraps(func)
    def calc_time(*args, **kwargs):

        begin = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        telapsed = end - begin

        try:
            PERFORMANCE_DATA[func.__name__].append(telapsed)
        except KeyError:
            PERFORMANCE_DATA[func.__name__] = [telapsed]

        print("Execution time of %s: %.3fs" % (func.__name__, telapsed) )

        return ret

    return calc_time


def get_performance_summary(prnt = True):

    summary = {}

    for func in PERFORMANCE_DATA.keys():
        summaryDat = {}
        perfList = PERFORMANCE_DATA[func]
        slowest = min(perfList)
        summaryDat["min"] = slowest
        fastest = max(perfList)
        summaryDat["max"] = fastest
        avg = stat.mean(perfList)
        summaryDat["avg"] = avg
        stdev = stat.stdev(perfList)
        summaryDat["stdev"] = stdev
        summary[func] = summaryDat

        if prnt:
            print("%s performance:\n%s" % (func, summaryDat))

    return summary


def print_frequencies():

    print("Supported FTDI frequencies:")
    freqList = [ "%0.1fHz" % freq for freq in FT_CLKDIV_LIST]
    print(freqList)


def print_mmdr(stAddr, valList):

    for idx, val in enumerate(valList):
        curAddr = stAddr + 2*idx
        print("addr:0x%04x,mmdr:%04x" % (curAddr, val))

