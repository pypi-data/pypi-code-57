import psycopg2
import time
import sys
from bytegain.custom.data_import.schema_info import REQUIRED_COLUMNS, ColumnInfo

class ConnectionFactory(object):
    def __init__(self, db_url):
        self._conn = None
        self._db_url = db_url

    def get_connection(self):
        try:
            # This is a trick to trigger error if connection is timed out
            if self._conn is not None and self._conn.isolation_level is not None:
                return self._conn
        except psycopg2.OperationalError as oe:
            print ("DB timeout: reconnecting")

        self._conn = psycopg2.connect(self._db_url)
        self._conn.autocommit = True
        # TODO - how to generalize this?
        self._conn.cursor().execute('set query_group TO "slow"')

        return self._conn

def create_table(cur, table_info, sortkey):
    columns = []
    for column in table_info.columns:
        columns.append("%s %s" % (column.name, column.datatype))

    drop = "drop table if exists %s" % (table_info.full_name)
    cur.execute(drop)
    create = "create table %s (%s) distkey(%s) sortkey(%s)" % (
            table_info.full_name, ", ".join(columns), sortkey, sortkey
    )
    print(create)
    cur.execute(create)

def copy_to_s3_from_redshift(cur, select, table_info, region, s3_secret_key, name):
    return copy_to_s3_from_redshift_by_bucket(cur, select, table_info, get_s3_bucket(region), s3_secret_key, name)

def copy_to_s3_from_redshift_by_bucket(cur, select, table_info, s3_bucket, s3_secret_key, name, destination_folder=""):
    start_time = time.time()
    statement = select.replace("'", "\\'")
    dest_csv = "%s/%s_%s/%s." % (destination_folder, table_info.schema, table_info.table, name)
    manifest = dest_csv + "manifest"
    statement = """
    unload('%s') to 's3://%s/%s'
    credentials 'aws_access_key_id=AKIAIGHWWWWWV534ALTA;aws_secret_access_key=%s'
    ALLOWOVERWRITE PARALLEL ON GZIP ESCAPE MANIFEST
    """ % (statement, s3_bucket, dest_csv, s3_secret_key)

    print("statement: %s" % statement)
    cur.execute(statement)
    sys.stdout.write(("Unloaded %s in %ds. " % (name, time.time() - start_time)))
    sys.stdout.flush()
    return manifest

def copy_from_s3(cur, table_info, manifest, region):
    manifest_url = 's3://%s/%s' % (get_s3_bucket(region), manifest)
    credentials = 'aws_iam_role=arn:aws:iam::087456767550:role/redshift-data-loader'
    upload_statement = "copy %s.%s from '%s' credentials '%s' MANIFEST ESCAPE GZIP COMPUPDATE ON EMPTYASNULL REGION '%s'" % (
            table_info.schema, table_info.table, manifest_url, credentials, region)
    upload_start = time.time()
    cur.execute(upload_statement)
    sys.stdout.write(("Uploaded %s.%s in: %ds.  " % (table_info.schema, table_info.table, time.time() - upload_start)))
    sys.stdout.flush()

def get_segment_tables(connection_factory, schema):
    conn = connection_factory.get_connection()
    cur = conn.cursor();
    cur.execute("select tablename from pg_tables where schemaname = '%s'" % schema)
    tables = []
    for row in cur:
        table = row[0]
        if table == "tracks":
            continue
        else:
            tables.append(table)

    return tables

def compute_table_info(connection_factory, table_info, where, exclude_common=None, no_groups=False,
                       force_required_columns = True, included_columns = None):
    """ Get ColumnInfos for all columns in table.
    """
    cur = connection_factory.get_connection().cursor()
    columns = get_meta_data(cur, table_info, True)
    if force_required_columns:
        for column in REQUIRED_COLUMNS:
            if column not in [c[0] for c in columns]:
                print("%s missing required column %s" % (table_info, column))
                return None

    excluded = exclude_common.columns if exclude_common else []
    excluded_set = set([x.name for x in excluded if x.name not in REQUIRED_COLUMNS])
    columns = [x for x in columns if x[0] not in excluded_set]
    if included_columns:
        new_columns = []
        for columnname in included_columns:
            for column in columns:
                if column[0] == columnname:
                    new_columns.append(column)
                    break
        columns = new_columns

    if len(columns) == 0:
        print("%s had no non-duplicate columns" % table_info)
        return table_info

    column_selects = []
    for column in columns:
        info = ColumnInfo(column[0], column[1])
        column_selects.extend(info.select_stats())
        table_info.add_column(info)

    if no_groups:
        return table_info

    sys.stdout.write("Counting %s                         \r" % table_info.table)
    sys.stdout.flush()
    where = table_info.get_full_where(where)
    select = "select count(1), %s from %s %s" % (",".join(column_selects), table_info.table, where)
    try:
        cur.execute(select)
    except psycopg2.ProgrammingError as e:
        print(e)
        print("error accessing table %s" % (table_info))
        return None
    row = cur.fetchone()
    items = iter(row)
    rows = next(items)
    table_info.set_rows(rows)
    for column_info in table_info.columns:
        column_info.read_stats(items)

    for column_info in table_info.columns:
        if column_info.is_numeric():
            select = 'select median("%s"), PERCENTILE_CONT ( 0.25 ) WITHIN GROUP (ORDER BY "%s"), '\
            'PERCENTILE_CONT ( 0.75 ) WITHIN GROUP (ORDER BY "%s")'\
            ' from %s %s' % (column_info.name, column_info.name, column_info.name, table_info.table, where)
            cur.execute(select)
            row = cur.fetchone()
            if row[0] is None:
                print("No median values for: %s " % column_info.name)
            else:
                column_info.median = float(row[0])
                column_info.percentile_25 = float(row[1])
                column_info.percentile_75 = float(row[2])
        else:
            print("%s is not numeric: %s" % (column_info.name, column_info.datatype))

    for column_info in table_info.columns:
        sys.stdout.write("Grouping %s.%s             \r" % (table_info.table, column_info.name))
        sys.stdout.flush()
        select = "select \"%s\", count(*) from %s %s group by 1 order by 2 desc limit 200" % (column_info.name, table_info.table, where)
        cur.execute(select)
        for row in cur:
            outcome = str(row[0], "UTF-8") if type(row[0]) == str else row[0]
            count = row[1]
            fraction = float(count) / table_info.row_count
            column_info.add_group(outcome, fraction)

    return table_info

def get_meta_data(cur, table_info, include_datatype = True):
    """ Get column meta data for table from DB cursor.
    """
    cur.execute("set search_path to '%s'" % table_info.schema)
    columns = []
    select = "select \"column\", \"type\" from pg_table_def where tablename = '%s'" % table_info.table
    cur.execute(select)
    # Ordering is important, so don't use hash/set
    for row in cur.fetchall():
        columns.append((row[0], row[1]) if include_datatype else row[0])
    return columns

def create_date_clause(start_date, end_date, tablename = None):
    # Create Where clause from start/end dates
    if tablename is None:
        column = "received_at"
    else:
        column = "%s.received_at" % tablename

    where = ""
    if start_date:
        where = "%s > timestamp '%s'" % (column, start_date)
    if end_date:
        if len(where) > 0:
            where = where + " AND "
        where = where + "%s < timestamp '%s'" % (column, end_date)
    return where

def and_where(w1, w2):
    if w1 and w2:
        return '(%s) AND (%s)' % (w1, w2)
    elif w1:
        return w1
    elif w2:
        return w2
    else:
        return None
