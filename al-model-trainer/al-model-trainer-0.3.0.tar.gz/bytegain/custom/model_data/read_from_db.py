"""
Reads rows from a cursor and converts into a dataset using buckets.
"""
import pyximport

pyximport.install()

import datetime
import itertools
import os
import time
import numpy
import psycopg2
import psycopg2.extras
import psycopg2.extensions
from hashlib import md5

import snowflake.connector
from snowflake.connector import DictCursor

import bytegain.custom.model_data.dataset as dataset
import bytegain.custom.model_data.row_handler as row_handler_module

import bytegain.custom.model_data.row_handler_proto.row_handler_pb2 as row_handler_pb2
from bytegain.custom.model_data.row_handler_proto.row_handler_pb2 import Extractor


def timestamp_to_epoch(value, curs, as_int=True):
    if value == None:
        return None
    # Sometimes these come in with fractional seconds, sometimes not.
    if '.' in value:
        dt = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f')
    else:
        dt = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    return int(time.mktime(dt.utctimetuple())) if as_int else dt


# Use floats instead of DECIMAL since floats are way faster
DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)

TIMESTAMP2EPOCH = psycopg2.extensions.new_type(
    psycopg2.DATETIME.values,
    'TIMESTAMP2EPOCH',
    timestamp_to_epoch)
psycopg2.extensions.register_type(TIMESTAMP2EPOCH)


def dates_as_timestamp(as_timestamp=True):
    TIMESTAMP2EPOCH = psycopg2.extensions.new_type(
        psycopg2.DATETIME.values,
        'TIMESTAMP2EPOCH',
        lambda value, curs: timestamp_to_epoch(value, curs, not as_timestamp))
    psycopg2.extensions.register_type(TIMESTAMP2EPOCH)


class ModSelector(object):
    def __init__(self, mods, test_mod, seed=1763):
        self._mods = mods
        self._test_mod = test_mod
        self._seed = seed

    def get_order_by(self, field):
        # return "order by sort_mod, interest_id"
        return "order by ((((%s + %d) * 7) * 17) * 103) %% 9999, %s" % (field, self._seed, field)

    def get_where(self, field, is_test):
        return "((((%s + %d) * 23) * 19) * 97) %% %d %s %d " % (
        field, self._seed, self._mods, "=" if is_test else "!=", self._test_mod)


class Selector(object):
    def __init__(self, table, where, label_field, id_field, secondary_sort=None, positive_outcome_rate_field = None, start_date=None, end_date = None):
        self._table = table
        self._label_field = label_field
        self._id_field = id_field
        self._secondary_sort = secondary_sort
        if positive_outcome_rate_field:
            term = "({label} or CORE.public.f_bucket_number({id}, 1000) < ({rate_field} * 1000))".format(
                label=self._label_field,
                id = self._id_field,
                rate_field = positive_outcome_rate_field)
            if where:
                where = where + " AND " + term
            else:
                where = term
        if start_date:
            where += " and value_at > "+ " '"+start_date + "' "
        if end_date:
            where += " and value_at < "+ " '"+ end_date + "' "
        self._where = where

    # Returns the where statement, or "" if there is no where select
    def get_where(self):
        return ("where %s" % self._where) if self._where is not None else ""

    # def create_statement(self, select):
    #     statement = "select %s, %s, %s from %s %s order by %s" % (
    #         self._id_field, self._label_field, select, self._table, self.get_where(),
    #         self._id_field if self._secondary_sort is None else ("%s, %s" % (self._id_field, self._secondary_sort)))
    #     # print statement
    #     return statement
    def create_statement(self, select):
        statement = "select %s, %s, %s from %s %s order by %s desc" % (
            self._id_field, self._label_field, select, self._table, self.get_where(),
            "value_at" if self._secondary_sort is None else ("%s, %s" % (self._id_field, self._secondary_sort)))
        # print statement
        return statement

    # def create_statement_for_queue(self, select, mod_selector, is_test):
    #     where = self._where
    #     if where is not None:
    #         where += " AND "
    #     where += mod_selector.get_where(self._id_field, is_test)
    #
    #     statement = "select %s, %s, %s from %s where %s %s" % (
    #         self._id_field, self._label_field, select, self._table, where, mod_selector.get_order_by(self._id_field))
    #     return statement


def create_connection(warehouse=None):
    return snowflake.connector.connect(
        account="apartmentlist.us-east-1",
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        warehouse=warehouse
    )


def feature_comments(config):
    cursor = create_connection().cursor()
    cursor.execute(f"DESCRIBE TABLE {config['table']}")
    return {r[0].lower(): r[9] for r in cursor.fetchall() if r[9]}


def generate_row_handler_stats(selector, row_handler):
    start_time = time.time()
    with create_connection() as connection:
        _extract_auto_params(connection, selector, row_handler)
    print("RowHandler stat time: %4.2fs" % (time.time() - start_time))


class IterableDataset(object):
    def __init__(self, statement, connection, row_handler, one_epoch=False):
        self._one_epoch = one_epoch
        self._row_handler = row_handler
        self._statement = statement
        self._connection = connection
        self._cursor = connection.cursor()
        self._initialize_cursor(True)

    def _initialize_cursor(self, update_row_handler=False):
        start_time = time.time()
        self._cursor.execute(self._statement)
        print("execute cursor time: %5.1fs" % (time.time() - start_time))
        if update_row_handler:
            self._header = [x.name for x in self._cursor.description]
            for bucket in self._row_handler._buckets:
                extractor = bucket._extractor
                extractor.update_fields_by_id(self._header)

    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.fetchone()
        if row is None:
            if self._one_epoch:
                raise StopIteration
            else:
                self._initialize_cursor()
                row = self._cursor.fetchone()
                if row is None:
                    # This happens only with empty query
                    raise StopIteration

        data = self._row_handler.get_data_from_row(row)

        zipped_row = dict(list(zip(self._header, row)))
        label = self._row_handler.get_label_from_row(zipped_row)
        id = self._row_handler.get_id_from_row(zipped_row)

        return data, label, id

    def __del__(self):
        self._connection.close()


def create_enqueue_operator(password, dbname, selector, row_handler, mod_selector, is_test=False):
    connection = create_connection(password, dbname)
    row_handler_module.set_fast_mode(True)
    start_time = time.time()
    statement = selector.create_statement_for_queue(get_select(row_handler), mod_selector, is_test)

    # For testing, we only iterate once through
    return IterableDataset(statement, connection, row_handler, one_epoch=is_test)


"""
if password is None, then password is read from ENV.
For instance if dbname=apartmentlist, then looks for ENV variable: APARTMENTLIST_PASS
"""


def create_datasets(selector, row_handler, test_fraction=0.10, row_limit=None, shuffle_rows = True):
    dates_as_timestamp(False)
    row_handler_module.set_fast_mode(True)
    categorical_indicies = row_handler.get_categorical_indicies()
    start_time = time.time()
    with create_connection() as connection:
        connection.autocommit = False
        # By default psycopg2 uses a client-side cursor which downloads all data before returning a single row
        with connection.cursor() as cursor:
            cursor.itersize = 100000
            statement = selector.create_statement(get_select(row_handler))
            if row_limit:
                statement = statement + (" limit %d" % row_limit)
            print("Statement: %s" % statement)
            cursor.execute(statement)
            cursor.fetchone()
            row_handler.replace_field_names_with_index(cursor)
            datasets = _create_datasets_from_cursor(cursor, row_handler, test_fraction, shuffle_rows)
    datasets.categorical_indicies = categorical_indicies
    print("Load time: %4.2fs" % (time.time() - start_time))
    return datasets

def create_test_datasets(selector, row_handler, row_limit=None, shuffle_rows = True):
    dates_as_timestamp(False)
    row_handler_module.set_fast_mode(True)
    categorical_indicies = row_handler.get_categorical_indicies()
    start_time = time.time()
    with create_connection() as connection:
        connection.autocommit = False
        # By default psycopg2 uses a client-side cursor which downloads all data before returning a single row
        with connection.cursor() as cursor:
            cursor.itersize = 100000
            statement = selector.create_statement(get_select(row_handler))
            if row_limit:
                statement = statement + (" limit %d" % row_limit)
            print("Statement: %s" % statement)
            cursor.execute(statement)
            cursor.fetchone()
            row_handler.replace_field_names_with_index(cursor)
            datasets = _create_test_datasets_from_cursor(cursor, row_handler, shuffle_rows)
    datasets.categorical_indicies = categorical_indicies
    print("Load time: %4.2fs" % (time.time() - start_time))
    return datasets    


def get_select(row_handler):
    selects = []
    for bucket in row_handler.buckets:
        extractor = bucket._extractor
        selects.append(apply_clamp(extractor))
        field2 = apply_clamp(extractor, field2=True)
        if field2:
            selects.append(field2)
    if row_handler._control_extractor:
        selects.extend(row_handler._control_extractor.get_fields())
    selects.extend(row_handler.extra_fields())
    return ",".join(selects)


def _create_datasets_from_cursor_multirow(cursor, multi_row_handler, test_fraction):
    print ("Creating multi-row")
    data = []
    labels = []
    ids = []
    count = 0
    start_time = time.time()
    for row in cursor:
        count += 1
        entry = multi_row_handler.process_row(row)
        if entry is not None:
            data.append(entry[0])
            labels.append(entry[1])
            ids.append(entry[2])

        if (count % 100000) == 0:
            print("%d -> %d" % (count, len(data)))

    print("rows: %d in %ds" % (len(data), time.time() - start_time))
    # data = numpy.array(data, dtype=numpy.float)
    labels = numpy.array(labels, dtype=numpy.float)
    ids = numpy.array(ids)
    # row_handler.print_summary()
    return data, labels, ids, multi_row_handler
    # return dataset.DataSets(multi_row_handler, data, labels, ids, test_fraction)


def _create_datasets_from_cursor(cursor, row_handler, test_fraction, shuffle_rows):
    data = []
    labels = []
    ids = []
    weights = []
    is_control = []
    for row in cursor:
        data.append(row_handler.get_data_from_row(row))
        labels.append(row_handler.get_label_from_row(row)[0])
        ids.append(row_handler.get_id_from_row(row))
        weights.append(row_handler.get_weight_from_row(row))
        is_control.append(row_handler.is_control_from_row(row))

    print("rows: %d" % len(data))
    data = numpy.array(data, dtype=numpy.float)
    labels = numpy.array(labels, dtype=numpy.float)
    ids = numpy.array(ids)
    weights = numpy.array(weights)
    is_control = numpy.array(is_control)
    row_handler.print_summary()
    return dataset.DataSets(row_handler, data, labels, ids, weights, test_fraction, shuffle_rows, is_control=is_control)

def _create_test_datasets_from_cursor(cursor, row_handler, shuffle_rows):
    data = []
    labels = []
    ids = []
    weights = []
    is_control = []
    for row in cursor:
        data.append(row_handler.get_data_from_row(row))
        labels.append(row_handler.get_label_from_row(row)[0])
        ids.append(row_handler.get_id_from_row(row))
        weights.append(row_handler.get_weight_from_row(row))
        is_control.append(row_handler.is_control_from_row(row))

    print("rows: %d" % len(data))
    data = numpy.array(data, dtype=numpy.float)
    labels = numpy.array(labels, dtype=numpy.float)
    ids = numpy.array(ids)
    weights = numpy.array(weights)
    is_control = numpy.array(is_control)
    row_handler.print_summary()
    return dataset.DataSets(row_handler, data, labels, ids, weights, test_fraction, shuffle_rows, is_control=True)


def apply_clamp(extractor, with_name=True, field2=False):
    if field2:
        field = extractor.get_field2()
        if field is None:
            # No field2, so do nothing
            return None
    else:
        field = extractor._field_name
    field_select = field
    if hasattr(extractor, "has_min") and extractor.has_min():
        field_select = "GREATEST(%s, %f)" % (field, extractor._min_val)
    if hasattr(extractor, "has_max") and extractor.has_max():
        field_select = "LEAST(%s, %f)" % (field_select, extractor._max_val)
    if field_select != field and with_name:
        field_select = "(case when %s is not null then %s else null end) as %s" % (field, field_select, field)
    return field_select


def _extract_auto_params(connection, selector, row_handler):
    # Pull out percentiles
    where = (selector._where + " AND") if selector._where else ""
    for bucket in row_handler.buckets:
        extractor = bucket._extractor
        if extractor._proto_type == Extractor.PERCENTILE_NORM:
            with connection.cursor() as cursor:
                # TODO(chris): Figure out a better abstraction for using selector._where.
                s = "select max(value), percentile from (select %s as value, ntile(100) over (order by %s asc) as percentile from bytegain_leads where %s %s is not null) group by 2 order by 2;" % (
                extractor._field, extractor._field, where, extractor._field)
                cursor.execute(s)
                percentiles = [float(x[0]) for x in cursor.fetchall()][0:-1]
                extractor.set_auto_values(percentiles)

    # Pull out categories for CategoryBucket
    for bucket in row_handler._buckets:
        if hasattr(bucket, "set_categories"):
            with connection.cursor() as cursor:
                s = "select %s, count(1) from %s where %s %s is not null group by 1 order by 2 desc" % (
                    bucket._extractor._field_name, selector._table, where, bucket._extractor._field_name)
                cursor.execute(s)
                categories = [{"name": x[0], "count": x[1]} for x in cursor.fetchall()]
                bucket.set_categories(categories)

    for bucket in row_handler._buckets:
        with connection.cursor() as cursor:
            s = "select %s from %s where %s %s is not null limit 1" % (
                bucket._extractor._field_name, selector._table, where, bucket._extractor._field_name)
            cursor.execute(s)
            # TODO(jjs): If all values are None?
            value = cursor.fetchone()[0]
            if isinstance(value, float):
                datatype = row_handler_pb2.Extractor.FLOAT
            elif isinstance(value, str):
                datatype = row_handler_pb2.Extractor.STRING
            elif isinstance(value, bool):
                datatype = row_handler_pb2.Extractor.BOOL
            elif isinstance(value, int) or isinstance(value, int):
                datatype = row_handler_pb2.Extractor.INT
            else:
                raise Exception("Unknown datatype: %s for %s" % (type(value), bucket._extractor._field_name))
            bucket._extractor._data_type = datatype

    select = ""
    for bucket in row_handler.buckets:
        extractor = bucket._extractor
        if hasattr(extractor, "_field"):
            field = extractor._field_name
            field_select = apply_clamp(extractor, with_name=False)
            select += "avg(case when %s is not null then 1.0 else 0.0 end) as %s, " % (field_select, field + "_null")
            if hasattr(extractor, "_sigma") and extractor._data_type is not row_handler_pb2.Extractor.STRING:
                if extractor._data_type == row_handler_pb2.Extractor.BOOL:
                    cast = "int::float"
                else:
                    cast = "float"
                select += ("stddev(%s::%s) as %s, avg(%s::%s) as %s, " % (
                field_select, cast, field + "_std", field_select, cast, field + "_avg"))
    if len(select) > 0:
        select = select[0:-2]
        full_statement = "select %s from %s %s" % (
            select, selector._table, ("where %s" % selector._where) if selector._where is not None else "")
        # print full_statement
        with connection.cursor(DictCursor) as cursor:
            cursor.execute(full_statement)
            row = cursor.fetchone()
            for bucket in row_handler.buckets:
                extractor = bucket._extractor
                if hasattr(extractor, "_field_name"):
                    field = bucket._extractor._field_name
                    extractor.set_null_fraction(row[field.upper() + "_NULL"])
                    if hasattr(extractor,
                               "set_auto_values") and extractor._data_type is not row_handler_pb2.Extractor.STRING:
                        std = row[field.upper() + "_STD"]
                        mean = row[field.upper() + "_AVG"]
                        bucket._extractor.set_auto_values(mean, std)
