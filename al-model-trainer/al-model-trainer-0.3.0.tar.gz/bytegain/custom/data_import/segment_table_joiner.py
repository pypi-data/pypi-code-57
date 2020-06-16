import psycopg2
import argparse
import time
import sys
import os
import tempfile
import gzip
from threading import Thread
from queue import Queue
import datetime
import io


parser = argparse.ArgumentParser(description='Joins a set of segment event tables together with main table')
parser.add_argument('--db', type=str, help='host:port:db:user:pass:schema:table', required=True)
parser.add_argument('--output_table', type=str, help='Table to create', required=True)
parser.add_argument('--input_tables', type=str, help='Comma-separated list of input tables', required=True)
parser.add_argument('--output_sortkeys', type=str, help='Sort/dist keys for output table', required=True)
parser.add_argument('--main_table', type=str, help='tracks table', required=True)
args = parser.parse_args()

src_conn, src_cur, schema, src_table = parse_params(args.db)

def parse_params(params):
    s = params.split(':')
    assert len(s) == 7
    conn = psycopg2.connect(host=s[0], port=s[1], dbname=s[2], user=s[3], password=s[4], sslmode='require')
    conn.autocommit = True
    cur = conn.cursor()
    if s[5]:
        cur.execute("set search_path to '%s'" % s[5])
    return conn, cur, s[5], s[6]

def get_meta_data(table):
    columns = []
    src_cur.execute("select \"column\" from pg_table_def where tablename = '%s'" % table)
    # Ordering is important, so don't use hash/set
    for row in src_cur.fetchall():
        name = row[0]
        columns.append(name)
    return columns

def get_columns():
    start_time = time.time()
    main_columns = get_meta_data(args.main_table)
    join_columns = {}

    for table in args.input_tables.split(','):
        columns = get_meta_data(table)
        included_columns = []
        for column in columns:
            if column not in main_columns and not column.startswith("context_"):
                if column in join_columns:
                    join_columns[column].append(table)
                else:
                    join_columns[column] = [table]

    return main_columns, join_columns

def create_joined_table(main_columns, join_columns):
    columns = []
    for column in main_columns:
        columns.append("%s.%s\n" % (args.main_table, column))

    for column in join_columns:
        tables = join_columns[column]
        if len(tables) == 1:
            columns.append(column)
        else:
            case = "case "
            for table in tables:
                case += "\twhen %s.%s is not null then %s.%s \n" % (table, column, table, column)
            case += "\telse NULL end as %s\n" % column
            columns.append(case)

    from_clause = "%s.%s\n" % (schema, args.main_table)
    for table in args.input_tables.split(","):
        from_clause += "left outer join %s.%s using (id)\n" % (schema, table)

    select = "select %s from %s" % (",".join(columns), from_clause)
    create = "create table %s as (%s) sortkey(%s) distkey(%s)" % (args.output_table, select, args.output_sortkeys, args.output_sortkeys)

    print("Create: %s" % create)
    src_cur.execute(create)

main_columns, join_columns = get_columns()
print(main_columns)
print(join_columns)
create_joined_table(main_columns, join_columns)
