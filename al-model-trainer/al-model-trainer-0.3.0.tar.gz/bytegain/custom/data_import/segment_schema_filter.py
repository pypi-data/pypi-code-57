import argparse
from bytegain.custom.data_import.schema_info import TableInfo, SchemaInfo, read_schema_from_file, save_schema
import math
import json

class SchemaFilter(object):
    def __init__(self):
        self.max_null = 0.95
        self.max_len = 40
        self.min_total_category_fraction = 0.10
        self.min_category_fraction = 0.01
        self.min_join_table_row_fraction = 0.01
        self.tables_to_keep = []
        self.tables_to_remove = []
        self.columns_to_keep = []
        self.ignored_events = []

    @staticmethod
    def load_from_json(json_file):
        with open(json_file, "r") as f:
            content = json.load(f)

        filter = SchemaFilter()
        filter.max_null = content['max_column_null']
        filter.max_len = content['max_avg_len']
        filter.min_total_category_fraction = content['min_total_category_fraction']
        filter.min_category_fraction = content['min_category_fraction']
        filter.min_join_table_row_fraction = content['min_join_table_row_fraction']
        filter.tables_to_keep = content['tables_to_keep']
        filter.tables_to_remove = content['tables_to_remove']
        filter.columns_to_keep = content['columns_to_keep']
        filter.ignored_events = content['ignored_events']
        filter.column_filters = content['column_filters']

        return filter

    def keep_column(self, table, column):
        return ("%s.%s" % (table, column)) in self.columns_to_keep

    def _filter_table(self, table, min_rows, is_tracks = False, debug = False):
        if table.table in self.tables_to_remove:
            return None
        elif table.table in self.tables_to_keep:
            pass
        elif table.row_count < min_rows:
            return None
        new_table = TableInfo(table.schema, table.table, where=table.where)
        new_table.set_rows(table.row_count)
        columns = table.columns
        # Computes the category minimum for this table based on # of table rows
        # relative to minimum rows.  The bigger a table, the lower the bar for
        # categories.
        row_ratio = table.row_count / float(min_rows)
        my_min = self.min_category_fraction / math.sqrt(row_ratio)
        for column in columns:
            if column.required():
                column._groups = []
            elif not self.keep_column(table.table, column.name):
                if column.null_fraction > self.max_null:
                    if debug:
                        print("%s.%s too many nulls: %5.3f > %5.3f" % (table.table, column.name, column.null_fraction, self.max_null))
                    continue
                if hasattr(column, 'col_length') and column.col_length > self.max_len:
                    if debug:
                        print("%s.%s too long: %5.3f > %5.3f" % (table.table, column.name, column.col_length, self.max_len))
                    continue
                if "timestamp" in column.datatype:
                    continue
                if debug:
                    print("%s is_groupable: %s" % (column.name, str(column.is_groupable())))
                if column.is_groupable():
                    category_total = 0
                    for category in column._groups:
                        if category[1] > my_min:
                            category_total += category[1]
                    if category_total < self.min_total_category_fraction:
                        if debug:
                            print(("%s category total: %f < %f (my_min: %f)" % (
                                column.name, category_total, self.min_total_category_fraction, my_min)))
                        continue
                    # pre_columns = column._groups
                    column._groups = [g for g in column._groups if g[1] > my_min]
                    if debug:
                        print("Groups for %s.%s: %s" % (table.table, column.name, str(column._groups)))
                    if len(column._groups) == 0:
                        continue

            if is_tracks and column.name == "event" and len(self.ignored_events) > 0:
                for event_name in self.ignored_events:
                    if event_name in column._groups:
                        column._groups.remove(event_name)

            new_table.add_column(column)

        if new_table.has_non_required() or new_table.table in self.tables_to_keep:
            return new_table
        else:
            print("No columns in %s" % new_table.table)
            return None

    def filter(self, schema_info):
        main_table = schema_info.main_table
        main_rows = main_table.row_count
        min_rows = main_rows * self.min_join_table_row_fraction
        # print "Min rows: %d" % min_rows
        filtered_main = self._filter_table(main_table, min_rows, is_tracks=True)
        filtered_pages = self._filter_table(schema_info.page_table, min_rows)
        join_tables = {}

        for table in list(schema_info.join_tables.values()):
            new_table = self._filter_table(table, min_rows)
            if new_table is not None:
                join_tables[table.table] = new_table

        new_schema_info = SchemaInfo(schema_info.schema, filtered_main, filtered_pages, join_tables)
        # new_schema_info.print_pretty()
        return new_schema_info

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Filter Schema down to reasonable columns/tables')
    parser.add_argument('--config', type=str, help='JSON filter config file', required=True)
    parser.add_argument('--input_schema', type=str, help='JSON schema file with all data', required=True)
    parser.add_argument('--output_schema', type=str, help='JSON schema file to output', required=True)

    args = parser.parse_args()
    schema = read_schema_from_file(args.input_schema)
    filter_config = SchemaFilter.load_from_json(args.config)
    small_schema = filter_config.filter(schema)
    small_schema.remove_columns(filter_config.column_filters)
    save_schema(args.output_schema, small_schema)
