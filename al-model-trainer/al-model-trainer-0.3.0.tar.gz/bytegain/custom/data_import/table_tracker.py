from collections import defaultdict
from numbers import Number

class ColumnTracker(object):
    """A ColumnTracker tracks information about a column and the values it contains.
    The number of occurrences of the first _max_items distinct values are counted.
    """
    def __init__(self, name, max_items):
        self._name = name
        self._max_items = max_items
        self._counts = defaultdict(int)
        self._total_non_null_count = 0
        self._total_count = 0
        self._datatype = None

    def add_entry(self, value):
        try:
            if self._datatype is None and value is not None:
                py_type = type(value)
                if py_type == str or py_type == str:
                    self._datatype = "varchar"
                elif py_type == bool or py_type == int:
                    self._datatype = "int"
                elif isinstance(value, Number):
                    self._datatype = "float"
                else:
                    self._datatype = str(py_type)

            if value in self._counts or len(self._counts) < self._max_items:
                self._counts[value] += 1

            self._total_count += 1
            if value is not None:
                self._total_non_null_count += 1
        except Exception as e:
            print("Could not add %s to %s: %s" % (str(value), self._name, str(e)))
            pass

    def get_top_values(self, min_percent):
        values = []
        min_count = self._total_count * min_percent
        for key, value in sorted(iter(list(self._counts.items())), key=lambda k_v: (k_v[1],k_v[0]), reverse = True):
            if value >= min_count and self._total_count > 0:
                values.append((key, value * 100.0 / self._total_count))

        return values

class TableTracker(object):
    """A TableTracker is a collection of ColumnTrackers for each column in a table.
    """
    def __init__(self, name, max_column_items, is_tracks = False):
        self._name = name
        self._max_column_items = max_column_items
        self._columns = {}
        self._total_count = 0
        self._no_userid  = 0
        self._is_tracks = is_tracks

    def _add_column(self, column_name, value):
        if column_name not in self._columns:
            self._columns[column_name] = ColumnTracker(column_name, self._max_column_items)
        self._columns[column_name].add_entry(str(value, "UTF-8") if type(value) == str else value)

    def _add_columns(self, iteritems, prefix = None):
        for column_name, value in iteritems:
            full_name = ("%s.%s" % (prefix, column_name)) if prefix else column_name
            if type(value) == dict:
                self._add_columns(iter(list(value.items())), prefix = full_name)
            elif type(value) in [list, tuple]:
                for entry in value:
                  self._add_columns([(column_name, entry)], prefix = prefix)                    
            else:
                self._add_column(full_name, value)

    def add_entry(self, values, has_userid):
        self._total_count += 1
        if not has_userid:
            self._no_userid += 1

        if self._is_tracks:
            self._add_columns([("event", values["event"])])
            self._add_columns(iter(list(values["context"].items())))
        else:
            self._add_columns(iter(list(values.items())))

    def print_pretty(self, min_percent):
        if self._total_count > 0:
            print("%s: %d [user_id: %3f%%]" % (self._name, self._total_count, 100 - (self._no_userid * 100.0 / self._total_count)))
        for key, column in sorted(iter(list(self._columns.items())), key=lambda k_v1: (k_v1[1]._total_count, k_v1[0]), reverse = True):
            if column._datatype is not None:
                if column._total_count > self._total_count * 0.02:
                    top_values = column.get_top_values(min_percent)
                    top_values = ["%s: %d%%" % (x[0], x[1]) for x in top_values]
                    print("    %14s: %s" % (key, str(top_values)))
