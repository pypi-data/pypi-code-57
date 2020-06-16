import psycopg2
import argparse
import time
import sys
import boto3
import os
import gzip
from datetime import date

class TableCloner(object):
    def __init__(self, table_info, where, client, src_region, s3_id, s3_secret_key, dest_dir = None, use_tablename_column = False):
        self._table_info = table_info
        self._src_schema = table_info.schema
        self._src_full_table = "%s.%s" % (self._src_schema, self._table_info.table)
        self._where = where
        self._s3_key_id = s3_id
        self._s3_secret_key = s3_secret_key
        self._client = client
        self._now = date.today()
        self._src_region = src_region
        self._dest_dir = dest_dir
        self._use_tablename_column = use_tablename_column

        if src_region == "us-east-1":
            self._s3_bucket = "bg-incoming-east"
        else:
            # TODO(jjs): Handle other regions
            self._s3_bucket = "bg-incoming-data"

    def get_s3_connection(self):
        return boto3.client('s3',
                aws_access_key_id=self._s3_key_id,
                aws_secret_access_key=self._s3_secret_key)

    def get_s3_dir(self):
        if self._dest_dir:
            return self._dest_dir
        else:
            date = self._now.strftime("%Y%m%d")
            return "%s/%s_data/%s" % (self._client, self._src_full_table, date)

    def get_where(self):
        return self._table_info.get_full_where(("WHERE %s" % self._where) if self._where else None)

    def get_select(self):   
        columns = ['"%s"' % x.name for x in self._table_info.columns]
        if self._use_tablename_column:
            columns.append("'%s'" % self._table_info.table)
        columns = ",".join(columns)
        return "select %s from %s %s" % (columns, self._src_full_table, self.get_where())

    def run_select_from_redshift(self, src_conn, gzip):
        src_cur = src_conn.cursor()
        start_time = time.time()
        statement = self.get_select()
        statement = statement.replace("'", "\\'")
        dest_csv = "%s/%s." % (self.get_s3_dir(), self._src_full_table)
        manifest = dest_csv + "manifest"
        statement = """
        unload('%s') to 's3://%s/%s'
        credentials 'aws_access_key_id=AKIAIGHWWWWWV534ALTA;aws_secret_access_key=%s'
        ALLOWOVERWRITE PARALLEL ON %s ESCAPE MANIFEST
        """ % (statement, self._s3_bucket, dest_csv, self._s3_secret_key, "GZIP" if gzip else "")

        # print ("statement: %s" % statement)
        src_cur.execute(statement)
        sys.stdout.write(("Unloaded %s in %ds. " % (self._src_full_table, time.time() - start_time)))
        sys.stdout.flush()
        self._table_info.set_s3_manifest("s3://%s/%s" % (self._s3_bucket, manifest))
        return manifest

    def copy_from_s3(self, dst_conn, dst_table, manifest):
        manifest_url = 's3://%s/%s' % (self._s3_bucket, manifest)
        credentials = 'aws_iam_role=arn:aws:iam::087456767550:role/redshift-data-loader'
        upload_statement = "copy %s from '%s' credentials '%s' MANIFEST ESCAPE GZIP COMPUPDATE ON EMPTYASNULL REGION '%s'" % (
                dst_table, manifest_url, credentials, self._src_region)
        upload_start = time.time()
        dst_cur = dst_conn.cursor()
        dst_cur.execute(upload_statement)
        sys.stdout.write(("Uploaded %s in: %ds.  " % (dst_table, time.time() - upload_start)))
        sys.stdout.flush()

    def clone_table(self, src_conn_factory, dst_conn_factory, dst_table_base, sort_key, skip_existing, incremental = False):
        sys.stdout.write("Working on: %s.. " % self._table_info.table)
        sys.stdout.flush()

        total_time = time.time()

        # Client is schema name
        dst_table = "%s.%s" % (self._client, dst_table_base)
        if skip_existing:
            try:
                dst_cur.execute("select 1 from %s" % dst_table)
                sys.stdout.write("Already exists... Skipping\n")
                return
            except:
                pass

        src_cur = src_conn_factory.get_connection().cursor()
        src_schema = self._src_schema

        col_formats = []
        for column in self._table_info.columns:
            col_desc = '%s %s' % (column.name, column.datatype)
            col_formats.append(col_desc)

        dist_text = ("distkey(%s)" % sort_key) if sort_key else ""
        sort_text = ("sortkey(%s)" % sort_key) if sort_key else ""
        if not incremental:
            dst_cur = dst_conn_factory.get_connection().cursor()
            dst_cur.execute("drop table if exists %s" % dst_table)
            create_str = "create table %s (%s) %s %s" % (dst_table, ', '.join(col_formats), dist_text, sort_text)
            # print ("Executing: %s" % create_str)
            dst_cur.execute(create_str)

        manifest = self.run_select_from_redshift(src_conn_factory.get_connection())
        self.copy_from_s3(dst_conn_factory.get_connection(), dst_table, manifest)

        print("Total clone time: %ds" % (time.time() - total_time))
        return True
