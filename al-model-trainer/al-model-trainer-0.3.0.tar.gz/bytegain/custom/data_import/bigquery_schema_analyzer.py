import time
#from google.cloud import storage
import argparse
from bytegain.custom.data_import.table_tracker import TableTracker
from bytegain.custom.data_import.schema_info import TableInfo, ColumnInfo, SchemaInfo, save_schema

from random import Random
from collections import defaultdict
from google.cloud import bigquery
import queue
import threading

print('##################################################')
print('WARNING: This code is has never been used for real')
print('##################################################')

class WorkerThread(threading.Thread):
    def __init__(self, query_queue, ignored_events):
        super(WorkerThread, self).__init__()
        self._client = bigquery.Client()
        self._query_queue = query_queue
        self._ignored_events = ignored_events
        self._event_types = defaultdict(int)
        self._page_table = TableTracker("page", 1000)
        self._tracks_table = TableTracker("tracks", 1000, is_tracks=False)
        self._other_count = defaultdict(int)
        self._event_tables = {}
        self._track_count = 0
        self._total_time = 0
        self._files = 0
        self._ignored_event_count = 0
        #self._start_time = time.mktime(args.start_date.utctimetuple()) if args.start_date else 0
        #self._end_time = time.mktime(args.end_date.utctimetuple()) if args.end_date else sys.maxint

        print("Ignored events: %s" % str(self._ignored_events))

    def total_count(self):
        return self._tracks_table._total_count

    def run(self):
        ended = False
        while not ended:
            item = self._query_queue.get()
            if not item:
                ended = True
            else:
                self.process_query(item)
            self._query_queue.task_done()

    def process_query(self, query):
        start_time = time.time()

        query_results = self._client.run_sync_query(query)
        query_results.use_legacy_sql = False
        query_results.use_query_cache = False

        query_results.run()

        schema = query_results.schema

        # Drain the query results by requesting a page at a time.
        page_token = None

        while True:
            rows, total_rows, page_token = query_results.fetch_data(
                max_results=100,
                page_token=page_token)

            for row in rows:
                self.process_row(row, schema)

            if not page_token:
                break
        self._total_time += (time.time() - start_time)
        self._files += 1

    def process_row(self, row, schema):
        """Process a top-level row of the table"""
        self._has_userid = "userId" in [field.name for field in schema]
        if args.require_user_id and not self._has_userid:
            return
        # Fake adding an entire row to increment Table's _total_count
        self._tracks_table.add_entry({}, self._has_userid)
        for index, value in enumerate(row):
            field = schema[index]
            self.process_column(value, field, "")

    def process_column(self, value, schema, column_name):
        """Process a top-level column of a row in the table"""
        if schema.mode == 'REPEATED':
            for index, value in enumerate(value):
                if schema.field_type == 'RECORD':
                    self.process_record(schema.name, value, schema.fields, column_name)
                else:
                    value_name = _column_name_join(column_name, schema.name)
                    self.analyze_value(value_name, schema.field_type, value)
        elif schema.field_type == 'RECORD':
            self.process_record(schema.name, value, schema.fields, column_name)
        else:
            value_name = _column_name_join(column_name, schema.name)
            self.analyze_value(value_name, schema.field_type, value)

    def process_record(self, name, value, schema, column_name):
        record_name = _column_name_join(column_name, name)
        schema_map={ field.name: field for field in schema }
        if value is not None:
            for k, v in list(value.items()):
                self.process_column(v, schema_map[k], record_name)

    def analyze_value(self, value_name, type, value):
        self._tracks_table._add_column(value_name, value)


def _column_name_join(left, right):
    return right if len(left) == 0 else ".".join([left, right])

def create_table_info(schema, table_tracker):
    table_info = TableInfo(schema, table_tracker._name)
    table_info.set_rows(table_tracker._total_count)
    #table_info.add_column(ColumnInfo("userId", "varchar"))
    #table_info.add_column(ColumnInfo("receivedAt", "timestamp"))

    for column_tracker in list(table_tracker._columns.values()):
        if column_tracker._datatype is None:
            continue

        name = column_tracker._name
        null_fraction = 1.0 - float(column_tracker._total_non_null_count) / table_tracker._total_count
        column = ColumnInfo(name, column_tracker._datatype)
        column.null_fraction = null_fraction

        top_values = column_tracker.get_top_values(0.00001)
        if len(top_values) > 0 and top_values[0] > 100:
            for value in top_values:
                column.add_group(value[0], value[1] / 100.0)

        table_info.add_column(column)
    return table_info


parser = argparse.ArgumentParser(description='Analyzes Segment JSON data in S3')
#parser.add_argument('--s3_src', type=str, help='s3 path of data ', nargs = '+', required=True)
#parser.add_argument('--s3_profile', type=str, help='s3 profile to use for data access', default = "s3_data_user")
parser.add_argument('--sample_ratio', type=float, help='fraction of data to read', default = 0.01)
#parser.add_argument('--start_date', type = segment_utils.as_date, help = 'Start date of data to analyze', default = None)
#parser.add_argument('--end_date', type = segment_utils.as_date, help = 'End date of data to analyze', default = None)
parser.add_argument('--sampling_seed', type = int, help = 'Random seed for sampling', default = 91876)
parser.add_argument('--max_files', type = int, help = 'Maximum files to sample', default = None)
parser.add_argument('--schema_info', type = str, help = 'SchemaInfo file to create', required = True)
#parser.add_argument('--filter_config', type=str, help='JSON filter config file', required=True)
parser.add_argument('--client', type = str, help = 'Client name', required = True)
parser.add_argument('--require_user_id', type = bool, help = "If true, then only count rows with userId set", default = False)

args = parser.parse_args()
rng = Random()
rng.seed(args.sampling_seed)

#filter_config = SchemaFilter.load_from_json(args.filter_config)

query_queue = queue.Queue(20)

thread = WorkerThread(query_queue, [])
thread.daemon = True
thread.start()
file_count = 0
start_time = time.time()
       
query_queue.put('SELECT * FROM `analytics-api-165801.138255571.ga_sessions_20170523` where totals.transactions > 0 limit 2')
query_queue.put(False)
query_queue.join()
print("Other types: %s" % str(thread._other_count))

print(thread._page_table.print_pretty(0.02))
print(thread._tracks_table.print_pretty(0.02))

# for table in sorted(thread._event_tables.values(), key = lambda (t): t._total_count, reverse = True):
#       if table._total_count > thread.total_count() * args.min_event_fraction:
#               print table.print_pretty(0.02)
#       else:
#               print "Skipping %s.  Too small %5.4f%%" % (table._name, table._total_count * 100.0 / thread.total_count())

track_info = create_table_info(args.client, thread._tracks_table)
page_info = create_table_info(args.client, thread._page_table)

# First pass, take filter min and use threshold 20x lower
#min_event_fraction = filter_config.min_join_table_row_fraction / 20
join_tables = {}
#for table_tracker in thread._event_tables.values():
#    if table_tracker._total_count > thread.total_count() * min_event_fraction:
#        join_tables[table_tracker._name] = create_table_info(args.client, table_tracker)

schema_info = SchemaInfo(args.client, track_info, page_info, join_tables)

save_schema(args.schema_info, schema_info)
