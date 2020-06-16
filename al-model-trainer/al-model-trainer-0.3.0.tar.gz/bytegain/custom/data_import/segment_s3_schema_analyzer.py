import time
import sys
import ujson
import gzip
import boto3
import os
from botocore.exceptions import ClientError
from google.cloud import storage
from apiclient import discovery, http
from googleapiclient.errors import HttpError
import argparse
import tempfile
import bytegain.data_import.segment_utils as segment_utils
from bytegain.custom.data_import.schema_info import TableInfo, ColumnInfo, SchemaInfo, save_schema

from bytegain.data_import.segment_schema_filter import SchemaFilter
from random import Random
from collections import defaultdict
import queue
import threading
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
            if value >= min_count:
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
        print("%s: %d [user_id: %3f%%]" % (self._name, self._total_count, 100 - (self._no_userid * 100.0 / self._total_count)))
        for key, column in sorted(iter(list(self._columns.items())), key=lambda k_v1: (k_v1[1]._total_count, k_v1[0]), reverse = True):
            if column._datatype is not None:
                if column._total_count > self._total_count * 0.02:
                    top_values = column.get_top_values(min_percent)
                    top_values = ["%s: %d%%" % (x[0], x[1]) for x in top_values]
                    print("    %14s: %s" % (key, str(top_values)))

class WorkerThread(threading.Thread):
    def __init__(self, file_queue, ignored_events):
        super(WorkerThread, self).__init__()
        self._file_queue = file_queue
        self._ignored_events = ignored_events
        self._event_types = defaultdict(int)
        self._page_table = TableTracker("page", 1000)
        self._tracks_table = TableTracker("tracks", 1000, is_tracks=True)
        self._other_count = defaultdict(int)
        self._event_tables = {}
        self._track_count = 0
        self._total_time = 0
        self._files = 0
        self._ignored_event_count = 0
        self._start_time = time.mktime(args.start_date.utctimetuple()) if args.start_date else 0
        self._end_time = time.mktime(args.end_date.utctimetuple()) if args.end_date else sys.maxsize

        print("Ignored events: %s" % str(self._ignored_events))

    def total_count(self):
        return self._tracks_table._total_count

    def run(self):
        ended = False
        while not ended:
            item = self._file_queue.get()
            if not item:
                ended = True
            else:
                self.process_file(item)
            self._file_queue.task_done()

    def process_file(self, file_name):
        start_time = time.time()
        input_file = gzip.open(file_name, "rb")
        for i, line in enumerate(input_file):
            content = ujson.loads(line)
            if "receivedAt" in content:
                # Remove trailing Z
                date = content["receivedAt"][0:-1]
                epoch = segment_utils.timestamp_to_epoch(date)
                if epoch < self._start_time or epoch > self._end_time:
                    break
            has_userid = "userId" in content
            if args.require_user_id and not has_userid:
                continue
            content_type = content["type"]
            self._event_types[content_type] += 1
            if content_type == "track":
                event_type = content["event"]
                if event_type in self._ignored_events:
                    self._ignored_event_count +=1
                    continue

                self._tracks_table.add_entry(content, has_userid)

                self._track_count += 1
                if event_type not in self._event_tables:
                    self._event_tables[event_type] = TableTracker(event_type, 1000)

                event_table = self._event_tables[event_type]
                if "properties" in content:
                    properties = content["properties"]
                    event_table.add_entry(properties, has_userid)
            elif content_type == "page":
                self._page_table.add_entry(content["properties"], has_userid)
            else:
                self._other_count[content_type] += 1

        self._total_time += (time.time() - start_time)
        self._files += 1
        os.remove(file_name)

def create_table_info(schema, table_tracker):
    table_info = TableInfo(schema, table_tracker._name)
    table_info.set_rows(table_tracker._total_count)
    table_info.add_column(ColumnInfo("userId", "varchar"))
    table_info.add_column(ColumnInfo("receivedAt", "timestamp"))

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

class S3Iterator(object):
    def __init__(self, s3_url):
        session = boto3.Session(profile_name=args.s3_profile)
        self._s3 = session.client('s3')
        self._bucket, self._key, _ = segment_utils.parse_s3_url(s3_url)
        self._file_iterator = None
        self._current_key = self._key

    def get_file(self, key):
        save_file = tempfile.NamedTemporaryFile(delete = False)
        try:
            self._s3.download_file(self._bucket, key, save_file.name)
            return save_file.name            
        except ClientError as e:
            print("Could not access: %s" % key)
            return None

    def __iter__(self):
        return self

    def _refresh_iterator(self):
        response = s3.list_objects_v2(Bucket=self._bucket, Prefix=self._key, StartAfter = self._current_key)
        # print "response: %s" % str(response)
        if "Contents" in response:
            contents = response["Contents"]
            print("Contents len: %d" % len(contents))
            self._file_iterator = contents.__iter__()

    def __next__(self):
        if self._file_iterator == None: 
            self._refresh_iterator()

        if self._file_iterator == None:
            raise StopIteration()

        try:           
            self._current_key = self._file_iterator.next()["Key"]
            return self._current_key
        except StopIteration:
            self._file_iterator = None
            return next(self)

class GSIterator(object):
    def __init__(self, gs_url):        
        gs_url = gs_url.replace('*', '')
        self._service = discovery.build('storage', 'v1')
        self._bucket_name, self._key, _ = segment_utils.parse_s3_url(gs_url)
        self._client = storage.Client()
        self._bucket = self._client.get_bucket(self._bucket_name)
        self._file_iterator = None
        self._page_token = None
        self._is_done = False

    def get_file(self, key, retry = True):
        with tempfile.NamedTemporaryFile(delete = False) as gz_file: 
            print("loading: %s" % key)
            try:
                req = self._service.objects().get_media(bucket=self._bucket_name, object=key)   
                downloader = http.MediaIoBaseDownload(gz_file, req)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                return gz_file.name
            except HttpError as e:
                if retry:
                    print("Error reading: %s.  Retrying" % key)
                    return get_file(key, False)
                else:
                    raise e

    def __iter__(self):
        return self

    def _refresh_iterator(self):
        print("Listing: %s" % self._key)
        if self._is_done:
            raise StopIteration
        blobs = self._bucket.list_blobs(prefix=self._key, page_token = self._page_token)
        self._page_token = blobs.next_page_token
        if self._page_token == None:
            self._is_done = True
        self._file_iterator = blobs.__iter__()

    def __next__(self):
        if self._file_iterator == None: 
            self._refresh_iterator()

        try:           
            blob = next(self._file_iterator)
            self._current_key = blob.name
            return self._current_key
        except StopIteration:
            self._refresh_iterator()            
            return next(self)

parser = argparse.ArgumentParser(description='Analyzes Segment JSON data in S3')
parser.add_argument('--s3_src', type=str, help='s3 path of data ', nargs = '+', required=True)
parser.add_argument('--s3_profile', type=str, help='s3 profile to use for data access', default = "s3_data_user")
parser.add_argument('--sample_ratio', type=float, help='fraction of data to read', default = 0.01)
parser.add_argument('--start_date', type = segment_utils.as_date, help = 'Start date of data to analyze', default = None)
parser.add_argument('--end_date', type = segment_utils.as_date, help = 'End date of data to analyze', default = None)
parser.add_argument('--sampling_seed', type = int, help = 'Random seed for sampling', default = 91876)
parser.add_argument('--max_files', type = int, help = 'Maximum files to sample', default = None)
parser.add_argument('--schema_info', type = str, help = 'SchemaInfo file to create', required = True)
parser.add_argument('--filter_config', type=str, help='JSON filter config file', required=True)
parser.add_argument('--client', type = str, help = 'Client name', required = True)
parser.add_argument('--require_user_id', type = bool, help = "If true, then only count rows with userId set", default = False)

args = parser.parse_args()
rng = Random()
rng.seed(args.sampling_seed)

filter_config = SchemaFilter.load_from_json(args.filter_config)

file_queue = queue.Queue(20)

thread = WorkerThread(file_queue, filter_config.ignored_events)
thread.daemon = True
thread.start()
file_count = 0
start_time = time.time()
       
for s3_path in args.s3_src:
    print("Processing: '%s'" % s3_path)
    files = S3Iterator(s3_path) if "s3://" in s3_path else GSIterator(s3_path)
    for start_key in files:
        if args.max_files != None and file_count >= args.max_files:
            break

        if rng.random() < args.sample_ratio:
            file_name = files.get_file(start_key)
            if file_name is not None:
                file_queue.put(file_name)
                file_count += 1
                if file_count % 10 == 0:
                    total_time = time.time() - start_time
                    sys.stdout.write("\r%d files in %ds (%5.3f/s)         " % (file_count, total_time, file_count / total_time))
                    sys.stdout.flush()

file_queue.put(False)
file_queue.join()
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
min_event_fraction = filter_config.min_join_table_row_fraction / 20
join_tables = {}
for table_tracker in list(thread._event_tables.values()):
    if table_tracker._total_count > thread.total_count() * min_event_fraction:
        join_tables[table_tracker._name] = create_table_info(args.client, table_tracker)

schema_info = SchemaInfo(args.client, track_info, page_info, join_tables)

save_schema(args.schema_info, schema_info)
