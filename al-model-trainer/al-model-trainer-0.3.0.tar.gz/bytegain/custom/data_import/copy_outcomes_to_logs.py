import psycopg2
import argparse
import time
import sys
import csv
import os
import tempfile
import gzip
from threading import Thread
from queue import Queue
import datetime

# Improve performance by not creating decimal objects - use native floats instead
DEC2FLOAT = psycopg2.extensions.new_type(
    psycopg2.extensions.DECIMAL.values,
    'DEC2FLOAT',
    lambda value, curs: float(value) if value is not None else None)
psycopg2.extensions.register_type(DEC2FLOAT)

# No need to convert strings -> timestamp -> string, just use string direct from input
DATE2STR = psycopg2.extensions.new_type(
    psycopg2.extensions.DATE.values,
    'DATE2STR', lambda value, curs: value)
psycopg2.extensions.register_type(DATE2STR)

parser = argparse.ArgumentParser(description='Clone a redshift db table')
parser.add_argument('--src', type=str, help='host:port:db:user:pass:schema:table', required=True)
parser.add_argument('--dst', type=str, help='host:port:db:user:pass:schema:table', required=True)
parser.add_argument('--label_column', type=str, help='Column containing outcome label', required=True)
parser.add_argument('--is_test', type=bool, default = False)

args = parser.parse_args()
BATCH_SIZE = 10000 if not args.is_test else 100

class Worker(Thread):
    def __init__(self, queue):
        super(Worker, self).__init__()
        self.daemon = True
        self._queue = queue

    def run(self):
        conn, cur, table = parse_params(args.dst)

        while True:
            records = self._queue.get()
            values = ["('%s', '%s', %d)" % (x[0], x[1], x[2]) for x in records]
            # print ("records: %s" % values)

            cur.execute('insert into %s values %s' % (table, ', '.join(values)))
            conn.commit()
            self._queue.task_done()

def parse_params(params):
    s = params.split(':')
    assert len(s) == 7
    conn = psycopg2.connect(host=s[0], port=s[1], dbname=s[2], user=s[3], password=s[4], sslmode='require')
    cur = conn.cursor()
    if s[5]:
        cur.execute("set search_path to '%s'" % s[5])
    return conn, cur, s[6]

def run_select():
    print ("Selecting from src")
    start_time = time.time()
    src_cur = src_conn.cursor('select')
    src_cur.itersize = 10000
    select = "select service_id, user_id, %s from %s where service_id is not null %s" % (
        args.label_column, src_table, "limit 377777" if args.is_test else "")
    src_cur.execute(select)
    print ("Queuing records")

    record_queue = Queue(6)
    for thread in range(2):
        worker = Worker(record_queue)
        worker.start()

    # format_string = '(%s)' % ', '.join(['%s'] * len(col_formats))
    rows = []
    chunks = 0
    row_count = 0
    current_file = None
    for row in src_cur:
        rows.append(row)
        row_count += 1
        if row_count % 10000 == 0:
            sys.stdout.write("Processed %d of %d rows in %ds    \r" % (row_count, src_cur.rowcount, time.time() - start_time))
            sys.stdout.flush()

        if row_count % BATCH_SIZE == 0:
            record_queue.put(rows)
            rows = []
            chunks += 1

    if len(rows) > 0:
        record_queue.put(rows)
        chunks += 1

    while record_queue.qsize() > 0:
        chunks_done = chunks - record_queue.qsize()
        runtime = time.time() - start_time
        rate = max(1, chunks_done * BATCH_SIZE / runtime)
        sys.stdout.write("Waiting for inserts: %3d ETA: %ds      \r " % (record_queue.qsize(), record_queue.qsize() * BATCH_SIZE / rate))
        sys.stdout.flush()
        time.sleep(2)

    record_queue.join()

print ("Connecting to src")
src_conn, src_cur, src_table = parse_params(args.src)
print ("Connecting to dest")
dst_conn, dst_cur, dst_table = parse_params(args.dst)
# Don't think schema changes are transactionable anyway..
# dst_conn.autocommit = True

print ("Recreating output table")
dst_cur.execute("drop table if exists %s" % dst_table)
create_str = "create table %s (service_id varchar(255), user_id varchar(255), outcome int)" % (dst_table)
dst_cur.execute(create_str)
dst_conn.commit()
run_select()
