import argparse
import datetime
import glob
import math
import os
import sys
import ujson as json
from collections import Counter

import flatten_json
import json_lines
from google.cloud import bigquery

from bytegain.custom.model_data import feature_analysis
from bytegain.custom.model_data.feature_analysis import Datatype, FeatureInfo, MIN_CATEGORY_FRACTION, MIN_CATEGORIES_FRACTION

# Features type enum
TYPE_LEASE = 'lease'
TYPE_SEARCH_RANK = 'search_rank'

LOG_FREQ = 10000
LOG_VERBOSE = sys.stdout.isatty()


def log_verbose(s):
    if LOG_VERBOSE:
        print(s)
        sys.stdout.flush()


# Copied from https://github.com/liyanage/python-modules/blob/master/running_stats.py
# Based on http://www.johndcook.com/standard_deviation.html, with some fixes to always use float.
class RunningStats:
    def __init__(self):
        self.n = 0
        self.old_m = 0.0
        self.new_m = 0.0
        self.old_s = 0.0
        self.new_s = 0.0

    def clear(self):
        self.n = 0

    def push(self, x):
        x = float(x)

        self.n += 1

        if self.n == 1:
            self.old_m = self.new_m = x
            self.old_s = 0.0
        else:
            self.new_m = self.old_m + (x - self.old_m) / self.n
            self.new_s = self.old_s + (x - self.old_m) * (x - self.new_m)

            self.old_m = self.new_m
            self.old_s = self.new_s

    def mean(self):
        return self.new_m if self.n else 0.0

    def variance(self):
        return self.new_s / self.n if self.n > 0 else 0.0

    def standard_deviation(self):
        return math.sqrt(self.variance())


class FeatureStats(object):
    """
    A FeatureStats is used to compute statistics on a feature.  It has a feature name, a count of the number of
    values added for the feature, an inferred value type, and an average value for numeric types.
    """

    def __init__(self, name):
        """
        :param name: the name of the feature
        """
        self._name = name
        self._count = 0
        self._db_type = None
        self._value_freq = Counter()  # XXX space is O(number of distinct values)
        self._running_stats = RunningStats()  # to compute stddev for number features
        self._median = None

    def add_value(self, value):
        """
        :param value: the value of the feature
        :return:
        """
        if type(value) == float:
            value = round(value, 4)

        self._count += 1

        if self._db_type is None and value is not None:
            if isinstance(value, str):
                self._db_type = str
            elif isinstance(value, bool):
                self._db_type = bool
            elif isinstance(value, int):
                self._db_type = int
            elif isinstance(value, float):
                self._db_type = float
            elif isinstance(value, datetime.datetime):
                self._db_type = datetime.datetime
            else:
                print('Unknown type: %s for %s' % (str(value), self._name))
                self._db_type = 0
        if self._db_type in (int, float) and isinstance(value, (int, float)):
            self._running_stats.push(value)
        self._value_freq[value] += 1

    def name(self):
        return self._name

    def total_count(self):
        return self._count

    def adjust_count(self, row_count):
        # _value_freq has a count for None only for explicit null values that were sent in a request, but missing
        # values are assumed null too so they should be counted up to row_count
        null_count = row_count - (self._count - self._value_freq[None])
        if null_count > 0:
            self._value_freq[None] = null_count
        # update total count to be total rows
        self._count = row_count

    def null_count(self):
        return self._value_freq[None]

    def not_null_count(self):
        return self.total_count() - self.null_count()

    def db_type(self):
        return self._db_type

    def average(self):
        return self._running_stats.mean()

    def median(self):
        if self._median is not None:
            return self._median
        if self._db_type in (int, float) and self.total_count() > 0:
            vals = list(self._value_freq.items())
            vals.sort() # sorts by key, but None may be first so remove it
            if vals[0][0] is None:
                vals = vals[1:]
            half_count = self.not_null_count() / 2
            sum = 0
            for val in vals:
                sum += val[1]
                if sum >= half_count:
                    self._median = val[0]
                    break
        return self._median

    def standard_deviation(self):
        return self._running_stats.standard_deviation()

    def sorted_value_frequencies(self):
        # return a list of tuples (key, value) by value desc.
        return self._value_freq.most_common()


def _process_feature(stats, row_count):
    """
    :param stats: a FeatureStats for a feature stored in db for user/model specified by data_info
    :param row_count: (int) the total number of entries in db for any feature matching data_info
    :return: a FeatureInfo
    """
    min_count = max(row_count * MIN_CATEGORY_FRACTION, 20)
    values = []
    category_sum = 0.0
    for value, count in stats.sorted_value_frequencies():
        if count > min_count:
            percent = count / float(row_count)
            values.append([value, percent, 0.0])
            category_sum += percent
        else:
            break

    if stats.db_type() in (bool, str):
        datatype = Datatype(stats.db_type(), len(values) > 1)
    elif stats.db_type() == float:
        # For now always assume int is non-categorical
        # TODO(jjs): Add normality test for ints to distinguish between categorical vs value
        if category_sum > 0.5 and len(values) > 1:
            is_category = True
        elif category_sum > MIN_CATEGORIES_FRACTION and len(values) > 2:
            is_category = True
        else:
            is_category = False
        datatype = Datatype(stats.db_type(), is_category)
    else:
        datatype = Datatype(stats.db_type(), False)

    null_fraction = stats.null_count() / float(row_count) if row_count > 0 else 0.0
    return FeatureInfo(stats.name(), datatype, values, 0.0, stats.average(), null_fraction,
                       stats.standard_deviation(), stats.median())


class StatsRunner:
    def __init__(self, row_generator):
        self._row_generator = row_generator

    def run(self):
        feature_stats = {}  # maps feature name to FeatureStats
        row_count = 0
        for row in self._row_generator:
            row_count += 1
            features = flatten_json.flatten(row)
            for name, value in list(features.items()):
                stats = feature_stats.get(name)
                if not stats:
                    stats = FeatureStats(name)
                    feature_stats[name] = stats
                stats.add_value(value)

        print('>>> Rows: %d' % row_count)

        features = []
        for name, stats in list(feature_stats.items()):
            stats.adjust_count(row_count)
            features.append(_process_feature(stats, row_count))

        features.sort(key=lambda row: row._column)
        features.sort(key=lambda row: row._datatype._is_cat)
        features.sort(key=lambda row: row._datatype._datatype)
        features.sort(key=lambda row: row._correlation, reverse=True)
        features.sort(key=lambda row: row.is_suitable(), reverse=True)
        if LOG_VERBOSE:
            is_suitable = True
            for feature in features:
                if is_suitable and not feature.is_suitable():
                    print ("\n--------------- EXCLUDED --------------\n")
                    is_suitable = False
                print("%s" % str(feature))

        return features


# Row generator from jsonl.gz files in local_dir.
def rows_from_jsonl_files(features_type, local_dir):
    row_count = 0
    if features_type == TYPE_LEASE:
        for infile in glob.glob(local_dir + '/*.jsonl.gz'):
            log_verbose('>>> Processing file: %s' % infile)
            with json_lines.open(infile) as f:
                for item in f:
                    row_count += 1
                    if row_count % LOG_FREQ == 0:
                        log_verbose('Rows: %d' % row_count)
                    row = json.loads(item['features'])
                    yield row
    elif features_type == TYPE_SEARCH_RANK:
        request_count = 0
        service_count = 0
        for infile in glob.glob(local_dir + '/*.jsonl.gz'):
            log_verbose('>>> Processing file: %s' % infile)
            with json_lines.open(infile) as f:
                for item in f:
                    request_count += 1
                    req_json = item['request']
                    services = json.loads(req_json)['services']
                    for service in services:
                        service_count += 1
                        user_data = service['user']
                        units_data = service['units']
                        for unit in units_data:
                            row_count += 1
                            row = unit.copy()
                            row.update(user_data)
                            yield row
                    if request_count % LOG_FREQ == 0:
                        log_verbose('Requests: %d, Services: %d, Rows: %d' % (request_count, service_count, row_count))

        print('>>> Requests: %d, Services: %d, Rows: %d' % (request_count, service_count, row_count))
    else:
        raise Exception('Unknown features_type: ' + features_type)


# Row generator from BQ query.
def rows_from_bq_query(features_type, query_where):
    if features_type == TYPE_LEASE:
        query = """SELECT features FROM `bg-rest-api.al.service_logs` WHERE """ + query_where
    elif features_type == TYPE_SEARCH_RANK:
        query = """SELECT request FROM `bg-rest-api.al.search_rank_logs` WHERE """ + query_where
    else:
        raise Exception('Unknown features_type: ' + features_type)

    print('>>> Query: %s' % query)

    bq_client = bigquery.Client(project='bg-rest-api')
    job_config = bigquery.QueryJobConfig()
    job_config.use_query_cache = True
    rows_iterator = bq_client.query_rows(query, job_config=job_config)

    row_count = 0
    if features_type == TYPE_LEASE:
        for qr in rows_iterator:
            features_json = qr[0]
            row = json.loads(features_json)
            row_count += 1
            if row_count % LOG_FREQ == 0:
                log_verbose('Rows: %d' % row_count)
            yield row
    elif features_type == TYPE_SEARCH_RANK:
        request_count = 0
        service_count = 0
        for qr in rows_iterator:
            request_count += 1
            req_json = qr[0]
            services = json.loads(req_json)['services']
            for service in services:
                service_count += 1
                user_data = service['user']
                units_data = service['units']
                for unit in units_data:
                    row_count += 1
                    row = unit.copy()
                    row.update(user_data)
                    yield row
            if request_count % LOG_FREQ == 0:
                log_verbose('Requests: %d, Services: %d, Rows: %d' % (request_count, service_count, row_count))

        print('>>> Requests: %d, Services: %d, Rows: %d' % (request_count, service_count, row_count))
    else:
        raise Exception('Unknown features_type: ' + features_type)


if __name__ == '__main__':
    LOG_VERBOSE = True
    parser = argparse.ArgumentParser(description='Analyze features from AL request logs.')
    parser.add_argument('--type', help='Type of features: lease, search_rank',
                        choices=[TYPE_LEASE, TYPE_SEARCH_RANK], required=True)
    where = parser.add_mutually_exclusive_group(required=True)
    where.add_argument('--local-dir', dest='local_dir', help="Local directory containing JSONL files")
    where.add_argument('--query-where', dest='query_where',
                       help='Standard SQL query WHERE clause to run against BigQuery')
    parser.add_argument('--output-file', dest='output_file', required=True,
                        help='Local file to save feature analysis to')
    args = parser.parse_args()

    row_generator = None
    if args.local_dir:
        local_dir = os.path.abspath(args.local_dir)
        print('Local dir: %s' % local_dir)
        row_generator = rows_from_jsonl_files(args.type, local_dir)
    else:
        # print('Query WHERE: %s' % args.query_where)
        row_generator = rows_from_bq_query(args.type, args.query_where)

    stats_runner = StatsRunner(row_generator)
    features = stats_runner.run()
    feature_analysis.save_features(args.output_file, features)

#
# WHERE clause examples:
#   _partitiontime = TIMESTAMP('2017-10-23')
# Inclusive range (2 days):
#   _partitiontime BETWEEN TIMESTAMP('2017-10-23') AND TIMESTAMP('2017-10-24')
#
