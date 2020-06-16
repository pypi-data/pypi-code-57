import time
import datetime
import sys
import json
import jsonpickle
from math import sqrt
import bytegain.custom.model_data.read_from_db as read_from_db
from bytegain.custom.model_data.bucket import CategoricalBucket, ValueBucket, StringBucket
from bytegain.custom.model_data.extractor import RowExtractor, DefaultedRowExtractor


def features_to_json(features):
    return json.dumps(json.loads(jsonpickle.encode(features)), sort_keys=True, indent=4)


def features_from_json(json_str):
    return jsonpickle.decode(json_str)


def save_features(filename, features):
    with open(filename, "w") as f:
        f.write(features_to_json(features))


def read_features(filename):
    with open(filename, "r") as f:
        json_str = f.read()
    return features_from_json(json_str)


class DataInfo(object):
    def __init__(self, selector, connection_uri=None):
        self._selector = selector
        self._connection_uri = connection_uri


class Datatype(object):
    def __init__(self, datatype, is_cat):
        self._is_cat = is_cat
        self._datatype = datatype

    def is_suitable(self):
        # bools & strings must be _is_cat
        if self._is_cat:
            return True
        if self._datatype in (bool, int, float):
            return True
        return False

    def data_type(self):
        return self._datatype

    def is_cat(self):
        return self._is_cat

    def is_number(self):
        return self._datatype in (int, int, float)

    def __str__(self):
        if self._datatype == str:
            type_str = "str"
        elif self._datatype == bool:
            type_str = "bool"
        elif self._datatype in (int, int):
            type_str = "int"
        elif self._datatype == float:
            type_str = "float"
        elif self._datatype == datetime.datetime:
            type_str = "timestamp"
        elif self._datatype == datetime.date:
            type_str = "date"
        else:
            return "Other: %s" % (str(self._datatype))

        return "%s%s" % (type_str, " (cat)" if self._is_cat else "")

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self._is_cat == other._is_cat and self._datatype == other._datatype

    def __ne__(self, other):
        return not self.__eq__(other)


class FeatureInfo(object):
    def __init__(self, column, datatype, top_values, correlation, average, null_fraction, stddev, median=0):
        self._column = column
        self._datatype = datatype
        self._top_values = top_values
        self._correlation = correlation
        self._average = average
        self._null_fraction = null_fraction
        self._stddev = stddev
        self._median = median

    def is_suitable(self):
        return self._datatype.is_suitable()

    def name(self):
        return self._column

    def data_type(self):
        return self._datatype

    def average(self):
        return self._average

    def median(self):
        return self._median

    def stddev(self):
        return self._stddev

    def top_values(self):
        return self._top_values

    def null_fraction(self):
        return self._null_fraction

    def create_bucket(self, is_category=None, one_hot=False, none_value=None):
        if not self.is_suitable():
            print("Warning- including %s which is marked as not suitable" % self._column)
        extractor = RowExtractor(self._column)
        if one_hot:
            return StringBucket(self._column, extractor, [x[0] for x in self._top_values])
        elif is_category != False and (is_category == True or self._datatype._is_cat):
            return CategoricalBucket(self._column, extractor, min_fraction=0.0001, none_value=none_value)
        else:
            # print "Using ValueBucket for %s (%f)" % (self._column, extractor)
            # extractor = AutoNormedExtractor(self._column, mu = self._average, sigma = self._stddev)
            return ValueBucket(self._column, extractor, has_null=False, default_value=none_value)

    def create_predict_script_bucket(self, is_category=None, one_hot=False, none_value=None):
        if not self.is_suitable():
            print("Warning- including %s which is marked as not suitable" % self._column)
        extractor = DefaultedRowExtractor(self._column)
        if one_hot:
            return StringBucket(self._column, extractor, [x[0] for x in self._top_values])
        elif is_category != False and (is_category == True or self._datatype._is_cat):
            bucket = CategoricalBucket(self._column, extractor, min_fraction=0.015, none_value=none_value)
            bucket.set_categories([{'name': x[0], 'count': 100 * x[1]} for x in self._top_values])
            return bucket
        else:
            # print "Using ValueBucket for %s (%f)" % (self._column, extractor)
            # extractor = AutoNormedExtractor(self._column, mu = self._average, sigma = self._stddev)
            return ValueBucket(self._column, extractor, has_null=False, default_value=none_value)

    def __str__(self):
        if self._datatype.is_cat():
            value_str = ("vals(%d):" % len(self._top_values)) + str(
                ["%s: %3.0f%%" % (str(x[0]), x[1] * 100) for x in self._top_values])
        elif self._datatype.is_number():
            value_str = "avg(%5.3f) median(%5.3f) stddev(%5.3f)" % (self.average(), self.median(), self.stddev())
        else:
            value_str = ("vals(%d)" % len(self._top_values)) +\
                        (":%s: %3.0f%%" % (str(self._top_values[0][0]), self._top_values[0][1] * 100) if self._top_values else '')
        return "%30.30s: null(%3.0f%%) %10s %5.3f %s" % (
            self._column, self._null_fraction * 100, str(self._datatype), sqrt(self._correlation) * 100, value_str)


MIN_CATEGORY_FRACTION = 0.03
MIN_CATEGORIES_FRACTION = 0.20

MIN_CATEGORY_STR_FRACTION = 0.0001
MIN_CATEGORIES_STR_FRACTION = 0.05

def _process_column(cursor, data_info, column, row_count, label_average):
    """
    Returns: a FeatureInfo
    """
    sys.stdout.write("Processing: %s                             \r" % column)
    sys.stdout.flush()
    min_count = max(row_count * MIN_CATEGORY_FRACTION, 500)
    min_str_count = max(row_count * MIN_CATEGORY_STR_FRACTION, 500)
    statement = "select \"%s\", count(*), avg(%s::int::float) from %s %s group by 1 order by 2 desc" % (
        column, data_info._selector._label_field, data_info._selector._table, data_info._selector.get_where())
    cursor.execute(statement)
    values = []
    db_type = None
    category_sum = 0
    for row in cursor:
        value = row[0]
        count = row[1]
        rate = row[2]

        if db_type == None and value is not None:
            if isinstance(value, str):
                db_type = str
            elif isinstance(value, bool):
                db_type = bool
            elif isinstance(value, int) or isinstance(value, int):
                db_type = int
            elif isinstance(value, float):
                db_type = float
            elif isinstance(value, datetime.datetime):
                db_type = datetime.datetime
                break
            elif isinstance(value, datetime.date):
                db_type = datetime.date
                break
            else:
                print("Unknown type: %s for %s" % (str(value), column))
                db_type = 0
                break

        if (db_type == str and count > min_str_count) or (count > min_count):
            percent = count / float(row_count)
            values.append([value, percent, rate])
            category_sum += percent
        elif db_type is not None:
            break

    if db_type in (bool, int, float):
        if db_type == bool:
            conversion = "::int::float"
        elif db_type == int:
            conversion = "::int"
        else:
            conversion = ""
        statement = """select avg("%s"%s),
        stddev("%s"::int::float),
        avg(case when "%s" is null then 1.0 else 0.0 end)
        from %s %s """ % (column, conversion, column, column, data_info._selector._table, data_info._selector.get_where())
    else:
        statement = "select 0, 1.0, avg(case when \"%s\" is null then 1.0 else 0.0 end) from %s %s" % (
            column, data_info._selector._table, data_info._selector.get_where())

    cursor.execute(statement)
    row = cursor.fetchone()
    avg = row[0]
    stddev = row[1]
    null_fraction = row[2]

    if db_type in (bool, str):
        datatype = Datatype(db_type, len(values) > 1)
    elif db_type == float:
        # For now always assume int is non-categorical
        # TODO(jjs): Add normality test for ints to distinguish between categorical vs value
        if category_sum > 0.5 and len(values) > 1:
            is_category = True
        elif category_sum > MIN_CATEGORIES_FRACTION and len(values) > 2:
            is_category = True
        else:
            is_category = False
        datatype = Datatype(db_type, is_category)
    else:
        datatype = Datatype(db_type, False)

    correlation = 0.0
    for value in values:
        correlation += value[1] * (label_average - value[2]) * (label_average - value[2])

    return FeatureInfo(column, datatype, values, correlation, avg, null_fraction, stddev)


def process_features(data_info):
    """
    Returns: a list of FeatureInfo
    """
    read_from_db.dates_as_timestamp(True)

    sys.stdout.write("Collecting features from: %s " % data_info._selector._table)
    sys.stdout.flush()
    start_time = time.time()
    features = []
    meta_statement = "select * from %s %s limit 1" % (data_info._selector._table, data_info._selector.get_where())
    connection = read_from_db.create_connection()
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute(meta_statement)
        columns = []
        for column in cursor.description:
            columns.append(column[0].lower())

        time1 = time.time()
        sys.stdout.write(" (%5.3fs)\n" % (time1 - start_time))
        sys.stdout.write("Counting rows: ")
        sys.stdout.flush()

        meta_statement = "select count(1), avg(%s::int::float) from %s %s " % (
            data_info._selector._label_field, data_info._selector._table, data_info._selector.get_where())
        cursor.execute(meta_statement)
        row = cursor.fetchone()
        row_count = row[0]
        label_average = row[1]
        time2 = time.time()
        sys.stdout.write("%d (%5.3fs)\n" % (row_count, time2 - time1))
        for column in columns:
            features.append(_process_column(cursor, data_info, column, row_count, label_average))

    time3 = time.time()
    print("Processing features: %5.3fs" % (time3 - time2))
    print("Total time: %5.3fs" % (time3 - start_time))

    features.sort(key=lambda row: row._column)
    features.sort(key=lambda row: row._datatype._is_cat)
    features.sort(key=lambda row: row._datatype._datatype.__name__)
    features.sort(key=lambda row: row._correlation, reverse=True)
    features.sort(key=lambda row: row.is_suitable(), reverse=True)
    is_suitable = True
    for feature in features:
        if is_suitable and not feature.is_suitable():
            print ("\n--------------- EXCLUDED --------------\n")
            is_suitable = False
        print("%s" % str(feature))

    return features
