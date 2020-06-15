import argparse
import logging
import os
from collections import OrderedDict
from datetime import datetime

from yqn_common.logger import NTLogger


class MyFormatter(logging.Formatter):
    converter = datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s


def set_logger(context, verbose=False):
    if os.name == 'nt':  # for Windows
        return NTLogger(context, verbose)

    logger = logging.getLogger(context)
    logger.setLevel(logging.DEBUG if verbose else logging.WARNING)
    formatter = MyFormatter(
        fmt='%(asctime)s;%(levelname)-.1s:' + context + ':\t[%(filename).25s:%(funcName).12s:%(lineno)4d]:%(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    console_handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(console_handler)
    return logger


class CappedHistogram:
    """Space capped dict with aggregate stat tracking.

    Evicts using LRU policy when at capacity; evicted elements are added to aggregate stats.
    Arguments:
    capacity -- the capacity limit of the dict
    """

    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.base_bins = 0
        self.base_count = 0
        self.base_min = float('inf')
        self.min_count = 0
        self.base_max = 0
        self.max_count = 0

    def __getitem__(self, key):
        if key in self.cache:
            return self.cache[key]
        return 0

    def __setitem__(self, key, value):
        if key in self.cache:
            del self.cache[key]
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self._evict()

    def total_size(self):
        return self.base_bins + len(self.cache)

    def __len__(self):
        return len(self.cache)

    def values(self):
        return self.cache.values()

    def _evict(self):
        key, val = self.cache.popitem(False)
        self.base_bins += 1
        self.base_count += val
        if val < self.base_min:
            self.base_min = val
            self.min_count = 1
        elif val == self.base_min:
            self.min_count += 1
        if val > self.base_max:
            self.base_max = val
            self.max_count = 1
        elif val == self.base_max:
            self.max_count += 1

    def get_stat_map(self, name):
        if len(self.cache) == 0:
            return {}
        counts = self.cache.values()
        avg = (self.base_count + sum(counts)) / (self.base_bins + len(counts))
        min_, max_ = min(counts), max(counts)
        num_min, num_max = 0, 0
        if self.base_min <= min_:
            min_ = self.base_min
            num_min += self.min_count
        if self.base_min >= min_:
            num_min += sum(v == min_ for v in counts)

        if self.base_max >= max_:
            max_ = self.base_max
            num_max += self.max_count
        if self.base_max <= max_:
            num_max += sum(v == max_ for v in counts)

        return {
            'avg_%s' % name: avg,
            'min_%s' % name: min_,
            'max_%s' % name: max_,
            'num_min_%s' % name: num_min,
            'num_max_%s' % name: num_max,
        }
