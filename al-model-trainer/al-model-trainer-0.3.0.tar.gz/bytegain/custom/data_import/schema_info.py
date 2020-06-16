import pickle
import json
import jsonpickle
import re

# timestamp and anonymous_id are in here because the beam joiner for CSV inputs expects them.
# TODO(chris): The right way to do this would be to pre-join CSV inputs on id.

REQUIRED_COLUMNS = ("id", "received_at", "timestamp", "anonymous_id")

class SchemaInfo(object):
    def __init__(self, schema, main_table, page_table, join_tables):
        self._schema = schema
        self._main_table = main_table
        self._page_table = page_table
        self._join_tables = join_tables

    @property
    def schema(self):
        return self._schema

    @property
    def main_table(self):
        return self._main_table

    @property
    def page_table(self):
        return self._page_table

    @property
    def join_tables(self):
        return self._join_tables

    @property
    def sorted_join_tables(self):
        return sorted(list(self._join_tables.values()), key = lambda v: (v._rows), reverse = True)

    def get_table(self, tablename):
        if tablename == self._main_table.table:
            return self._main_table
        elif tablename == self._page_table.table:
            return self._page_table
        else:
            return self._join_tables[tablename]

    def print_pretty(self):
        print("\nSchema: %s" % self._schema)
        self._main_table.print_pretty()
        self._page_table.print_pretty()

        for join_table in sorted(list(self.join_tables.values()), key = lambda v: v.row_count, reverse=True):
            join_table.print_pretty()

    def remove_table(self, tablename):
        self._join_tables.remove(tablename)

    def remove_columns(self, columns):
        for column_full in columns:
            tablename, columnname = column_full.split(".", 1)
            column_pattern = re.compile(columnname)
            if tablename == "*":
                tables = [self._main_table, self._page_table] + list(self._join_tables.values())
            else:
                tables = [self.get_table(tablename)]
            matches = 0

            for table in tables:
                columns = []
                for column in table.columns:
                    if column_pattern.match(column.name):
                        columns.append(column.name)
                for column in columns:
                    table.remove_column(column)
                matches += len(columns)
            # if matches == 0:
            #       print ("%s not found" % column_full)
            # else:
            #       print ("%s removed %d times" % (column_full, matches))

    def translate_schema_tablenames(self, new_schema):
        """ Translates table names from Blah.XXX to NEW_SCHEMA.Blah_XXX
        """
        self._main_table._table = "%s_%s" % (self._schema, self._main_table._table)
        self._main_table._schema = new_schema
        new_join_table = {}
        for table in list(self._join_tables.values()):
            table._table = "%s_%s" % (self._schema, table._table)
            table._schema = new_schema
            new_join_table[table._table] = table

        self._join_tables = new_join_table
        self._schema = new_schema

class TableInfo(object):
    def __init__(self, schema, table, where = None):
        self._schema = schema
        self._table = table
        self._rows = None
        self._columns = []
        self._column_to_index = None
        self._where = where
        self._s3_manifest = None

    def set_rows(self, rows):
        self._rows = rows

    def set_s3_manifest(self, manifest_url):
        self._s3_manifest = manifest_url

    @property
    def schema(self):
        return self._schema

    @property
    def table(self):
        return self._table

    @property
    def full_name(self):
        return "%s.%s" % (self._schema, self._table)

    @property
    def row_count(self):
        return self._rows

    @property
    def where(self):
        return self._where

    def get_full_where(self, input_where):
        # Hack for backwards compatibility with pickle
        if not hasattr(self, "_where"):
            self._where = None
        input_empty = input_where == None or len(input_where) == 0
        if input_empty and self._where == None:
            return ""
        elif self._where and input_empty:
            return "WHERE %s" % self._where
        elif self._where is None:
            return input_where
        else:
            return "%s AND %s" % (input_where, self._where)

    @property
    def columns(self):
        return self._columns

    def has_column(self, column):
        for x in self.columns:
            if column == x.name:
                return True

        return False

    def get_column(self, columnname):
        index = self.get_column_index(columnname)
        return self._columns[index]

    def get_column_index(self, columnname):

        if not hasattr(self, "_column_to_index") or self._column_to_index == None:
            self._column_to_index = {}         
            for i, column in enumerate(self._columns):
                self._column_to_index[column.name] = i

        return self._column_to_index[columnname]

    def add_column(self, column):
        self._column_to_index = None                
        self._columns.append(column)

    def remove_column(self, columnname):
        column = self.get_column(columnname)
        self._column_to_index = None                
        self._columns.remove(column)

    def __str__(self):
        return "%s: (%s)" % (self.full_name, str(self._rows) if self._rows else "N/A")

    def has_non_required(self):
        for x in self._columns:
            if not x.required():
                return True

        return False

    def print_pretty(self):
        print("\n\n%s" % self)
        if self.row_count > 0:
            for column in self._columns:
                val = column.print_pretty()
                if type(val) != str:
                    print(str(val).encode("utf-8"))


def is_db_type_numeric(datatype):
    return "float" in datatype or "double" in datatype or "int" in datatype or "numeric" in datatype


class ColumnInfo(object):
    def __init__(self, name, datatype):
        self.name = name
        self.datatype = datatype
        self._groups = []
        self.col_length = 0
        self.null_fraction = 0

    def required(self):
        return self.name in REQUIRED_COLUMNS


    def is_numeric(self):
        return is_db_type_numeric(self.datatype)


    def select_stats(self):
        quoted_name = "\"%s\"" % self.name
        selects = ["avg((%s is null)::int::float) as %s_null" % (quoted_name, self.name)]
        if "char" in self.datatype:
            selects.append("avg(length(%s)) as %s_len" % (quoted_name, self.name))
        if self.is_numeric():
            selects.append("avg(%s) as %s_ave, VARIANCE(%s) as %s_var" % (
                quoted_name, self.name, quoted_name, self.name))

        return selects

    def is_groupable(self):
        return ("char" in self.datatype or
                (("int" in self.datatype or "float" in self.datatype) and len(self._groups) > 1 and
                        self.groups_sum() - self._groups[0][1] > 0.005 ))
    def add_group(self, group, fraction):
        self._groups.append((group, fraction))

    def groups_sum(self):
        return sum([x[1] for x in self._groups])

    def read_stats(self, items):
        self.null_fraction = next(items)
        if "char" in self.datatype:
            self.col_length = next(items)
            if self.col_length is None:
                self.col_length = 0
        if self.is_numeric():
            self.average = next(items)
            self.variance = next(items)

    def __str__(self):
        return self.print_pretty()

    def print_pretty(self):
        dt = self.datatype.split(" ")[0]
        if len(dt) > 12:
            dt = dt[0:12]

        if len(self.name) > 30:
            name = self.name[-30:]
        else:
            name = self.name
        base = "  %30s(%s): " % (name, dt)
        if self.null_fraction is None:
            return "%42s: No Info" % (base)

        if "char" in self.datatype:
            base = "%42s %3d%% %3d" % (base, self.null_fraction * 100, self.col_length)
        else:
            base = "%42s %3d%%" % (base, self.null_fraction * 100)

        if self.is_groupable():
            grouping = []
            for group in self._groups:
                fraction = group[1]
                if fraction > 0.001:
                    grouping.append("%s: %2d%%" % (group[0], fraction * 100))

            base = base + " [%s]" % ",".join(grouping)

        return base


def read_old_schema_from_file(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

def read_schema_from_file(filename):
    with open(filename, "rb") as f:
        schema = jsonpickle.decode(json.dumps(json.load(f)))
        # TODO(jjs) - remove this hack for backwards compatibility
        if not hasattr(schema, '_page_table'):
            schema._page_table = schema.get_table('pages')
            del schema._join_tables['pages']
        return schema

def save_schema(filename, schema, compact = False):
    with open(filename, "wb") as f:
        # indent=0 is just a few percent bigger than indent=None, and make the  half readable.
        # indent=2 is about 2x the size.
        json.dump(json.loads(jsonpickle.encode(schema)), f, sort_keys=True, indent = 0 if compact else 2)

