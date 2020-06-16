import psycopg2
import argparse
import time
import sys
import csv
import boto3
import os
import tempfile
import gzip
from threading import Thread
from queue import Queue
import datetime
import io

# Improve performance by not creating decimal objects - use native floats instead
DEC2FLOAT = psycopg2.extensions.new_type(
                psycopg2.extensions.DECIMAL.values,
                'DEC2FLOAT',
                lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)

# No need to convert strings -> timestamp -> string, just use string direct from input
def parse_date(str_val, cursor):
    if str_val is None:
        return None
    return str_val
    # values = str_val.split("-")
    # return "%d-%02d-%02d" % (values[0], values[1], values[2])
    # return datetime.datetime(int(values[0]), int(values[1]), int(values[2]))

DATE2TIMESTAMP = psycopg2.extensions.new_type(
                psycopg2.extensions.DATE.values,
                'DATE2TIMESTAMP', parse_date)
psycopg2.extensions.register_type(DATE2TIMESTAMP)


parser = argparse.ArgumentParser(description='Clone a redshift db table')
parser.add_argument('--src', type=str, help='host:port:db:user:pass:schema:table', required=True)
parser.add_argument('--dst', type=str, help='host:port:db:user:pass:schema:table', required=True)
parser.add_argument('--s3_key_id', type=str, help='AWS user id for S3', required=True)
parser.add_argument('--s3_secret_key', type=str, help='AWS secret key for S3', required=True)
parser.add_argument('--is_test', type=bool, default = False)
parser.add_argument('--where', type=str, default = None, help = "Where clause limiting data import")
parser.add_argument('--upload_threads', type=int, default = 1, help = "Number of threads to use for uploading data")
parser.add_argument('--client', type=str, required = True, help = "Name of client this table is for")
parser.add_argument('--mod_column', type=str, required = True, help = "Column to mod table by")
parser.add_argument('--columns', type=str, default=None, help ="Comma seperated list of column to copy.  If not set all columns are copied")
parser.add_argument('--from_redshift', type=bool, default = True, help = "Set if src is a redshift table")
parser.add_argument('--src_region', type=str, default ='us-east-1', help = "AWS region where src Redshift is")
parser.add_argument('--distcolumn', type=str, default = None, help = "Dist column for created table")
parser.add_argument('--sortcolumn', type=str, default = None, help = "Sort column for created table")
args = parser.parse_args()
BATCH_SIZE = 50000 if not args.is_test else 10000

if args.src_region == "us-east-1":
    S3_BUCKET = "bg-incoming-east"
else:
    # TODO(jjs): Handle other regions
    S3_BUCKET = "bg-incoming-data"

def get_s3_connection():
    return boto3.client('s3',
            aws_access_key_id=args.s3_key_id,
            aws_secret_access_key=args.s3_secret_key)

def get_s3_dir(client, table, now):
    date = now.strftime("%Y%m%d")
    return "%s/%s_data/%s" % (client, table, date)

class Worker(Thread):
    def __init__(self, table, date, queue, output_files):
        super(Worker, self).__init__()
        self.daemon = True
        self._queue = queue
        self._table = table
        self._date = date
        self._output_files = output_files

    def run(self):
        s3 = get_s3_connection()

        while True:
            chunk_count, rows = self._queue.get()
            with tempfile.NamedTemporaryFile(suffix = ".csv.gz", delete = False) as file:
                gz_file = gzip.GzipFile(fileobj=file, compresslevel=5)
                csv_file = csv.writer(gz_file, quotechar = None, delimiter = '|', quoting = csv.QUOTE_NONE, escapechar='\\')
                for row in rows:
                    output_row = []
                    csv_file.writerow(row)

                gz_file.close()
            with open(file.name, "r") as upload_file:
                key = "%s/%s_%04d.csv.gz" % (get_s3_dir(args.client, self._table, self._date), self._table, chunk_count)
                # print ("file %s bucket: %s key: %s" % (file.name, S3_BUCKET, key))

                s3.put_object(Bucket = S3_BUCKET, Key = key, Body = upload_file)
                self._output_files.append(key)
                self._queue.task_done()
                os.remove(file.name)

def parse_params(params):
    s = params.split(':')
    assert len(s) == 7
    conn = psycopg2.connect(host=s[0], port=s[1], dbname=s[2], user=s[3], password=s[4], sslmode='require')
    conn.autocommit = True
    cur = conn.cursor()
    if s[5]:
        cur.execute("set search_path to '%s'" % s[5])
    return conn, cur, s[6]

def get_select(selected_columns, add_mods):
    where = args.where if args.where else ""
    if add_mods:
        where = where + (" AND " if args.where is not None else "") + "mod(%s,%d) = %%(mods)s" % (args.mod_column, mods)

    if len(where) > 0:
        where = "WHERE %s" % where

    return "select %s from %s %s" % (",".join(selected_columns) if selected_columns is not None else "*", src_table, where)

def run_select_from_redshift(now, selected_columns):
    start_time = time.time()
    src_cur.execute('set query_group TO "slow"')
    statement = get_select(selected_columns, False)
    statement = statement.replace("'", "\\'")
    dest_csv = "%s/%s." % (get_s3_dir(args.client, src_table, now), dst_table)
    manifest = dest_csv + "manifest"
    statement = """
    unload('%s') to 's3://%s/%s'
    null as '__NULL_VALUE__'
    credentials 'aws_access_key_id=AKIAIGHWWWWWV534ALTA;aws_secret_access_key=%s'
    ALLOWOVERWRITE PARALLEL ON GZIP ESCAPE MANIFEST
    """ % (statement, S3_BUCKET, dest_csv, args.s3_secret_key)

    print("statement: %s" % statement)
    src_cur.execute(statement)
    return manifest

def run_select(now, selected_columns):
    s3_files = []
    start_time = time.time()
    print ("Counting rows")
    src_cur.execute('set query_group TO "slow"')
    src_cur.execute("select count(1) from %s %s" % (src_table, ("WHERE %s" % args.where) if args.where else ""))
    row_count = src_cur.fetchone()[0]
    mods = row_count / 100000
    base_statement = get_select(selected_columns, True)
    print("Statement: %s" % base_statement)
    print("Processing %d rows in %d steps" % (row_count, mods))

    record_queue = Queue(args.upload_threads)
    for thread in range(args.upload_threads):
        worker = Worker(dst_table, now, record_queue, s3_files)
        worker.start()

    format_string = '(%s)' % ', '.join(['%s'] * len(col_formats))
    rows = []
    chunks = 0
    row_count = 0
    for mod in range(mods):
        src_cur.execute(base_statement, {'mods': mod})
        for row in src_cur:
            rows.append(row)
            row_count += 1
            if row_count % 10000 == 0:
                sys.stdout.write("Processed %d rows in %ds    \r" % (row_count, time.time() - start_time))
                sys.stdout.flush()

            if row_count % BATCH_SIZE == 0:
                record_queue.put((chunks, rows))
                rows = []
                chunks += 1

    if len(rows) > 0:
        record_queue.put((chunks, rows))
        chunks += 1

    print("")
    while record_queue.qsize() > 0:
        chunks_done = chunks - record_queue.qsize()
        runtime = time.time() - start_time
        rate = max(1, chunks_done * BATCH_SIZE / runtime)
        sys.stdout.write("Waiting for files to upload: %3d ETA: %ds      \r " % (record_queue.qsize(), record_queue.qsize() * BATCH_SIZE / rate))
        sys.stdout.flush()
        time.sleep(2)

    record_queue.join()
    return s3_files

def copy_from_s3(manifest):
    manifest_url = 's3://%s/%s' % (S3_BUCKET, manifest)
    print("Manifest: %s" % manifest_url)
    credentials = 'aws_iam_role=arn:aws:iam::087456767550:role/redshift-data-loader'
    upload_statement = "copy %s from '%s' credentials '%s' MANIFEST ESCAPE GZIP COMPUPDATE ON null as '__NULL_VALUE__' REGION '%s'" % (
            dst_table, manifest_url, credentials, args.src_region)
    upload_start = time.time()
    print("Upload: %s" % upload_statement)
    dst_cur.execute(upload_statement)
    print("Upload time: %5.3fs" % (time.time() - upload_start))

total_time = time.time()
now = datetime.datetime.today()
print ("Connecting to SRC and DEST")
src_conn, src_cur, src_table = parse_params(args.src)
dst_conn, dst_cur, dst_table = parse_params(args.dst)

# Don't think schema changes are transactionable anyway..
# dst_conn.autocommit = True

print ("Creating DST table")
src_cur.execute("select * from pg_table_def where tablename = '%s'" % src_table)
# Ordering is important, so don't use hash/set
if args.columns is not None:
    selected_columns = str.split(args.columns, ',')
    col_formats = [""] * len(selected_columns)
else:
    selected_columns = None
    col_formats = []

for row in src_cur.fetchall():
    name = row[2]
    datatype = row[3]
    col_desc = '%s %s' % (name, datatype)
    if selected_columns is None:
        col_formats.append(col_desc)
    elif name in selected_columns:
        index = selected_columns.index(name)
        if index is not None:
            col_formats[index] = col_desc

if args.from_redshift:
    manifest = run_select_from_redshift(now, selected_columns)
    # manifest = "apartmentlist/lead_scoring_set_with_model_data/20171115/bytegain_leads.manifest"
else:
    s3_files = run_select(now, selected_columns)


dist_text = ("distkey(%s)" % args.distcolumn) if args.distcolumn else ""
sort_text = ("sortkey(%s)" % args.sortcolumn) if args.sortcolumn else ""
dst_cur.execute("drop table if exists %s" % dst_table)
create_str = "create table %s (%s) %s %s" % (dst_table, ', '.join(col_formats), dist_text, sort_text)
print("Executing: %s" % create_str)
dst_cur.execute(create_str)

if args.from_redshift:
    manifest_url = copy_from_s3(manifest)
else:
    print("\nCopying to S3")
    with tempfile.NamedTemporaryFile(suffix = "manifest.json", delete = False) as f:
        f.write('{"entries": [\n')
        text = ',\n'.join(['{"url":"s3://%s/%s","mandatory":true}' % (S3_BUCKET, entry) for entry in s3_files])
        f.write(text)
        f.write("\n]\n}")
        s3 = get_s3_connection()
        manifest_key = "%s/%s.manifest" % (get_s3_dir(args.client, src_table, now), dst_table)
        f.flush()
        f.seek(0)
        s3.put_object(Bucket = S3_BUCKET, Key = manifest_key, Body = f)

    manifest_url = 's3://%s/%s' % (S3_BUCKET, manifest_key)
    credentials = 'aws_iam_role=arn:aws:iam::087456767550:role/redshift-data-loader'
    upload_statement = "copy %s from '%s' credentials '%s' MANIFEST ESCAPE GZIP COMPUPDATE ON EMPTYASNULL;" % (dst_table, manifest_url, credentials)
    upload_start = time.time()
    dst_cur.execute(upload_statement)
    print("Upload time: %5.3fs" % (time.time() - upload_start))

print("Total clone time: %ds" % (time.time() - total_time))
