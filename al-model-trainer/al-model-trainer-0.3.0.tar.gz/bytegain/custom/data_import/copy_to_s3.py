import argparse
import bytegain.custom.data_import.schema_info as schema_info
import bytegain.custom.data_import.db_utils as db_utils
import pickle
import io
import boto3

parser = argparse.ArgumentParser(description='Copies table from redshift to s3')
parser.add_argument('--src_url', type=str, help='db url', required=True)
parser.add_argument('--schema', type = str, help = 'schema of table to copy', required = True)
parser.add_argument('--table', type = str, help = 'table name to copy', required = True)
parser.add_argument('--s3_key_id', type=str, help='AWS user id for S3', required=True)
parser.add_argument('--s3_secret_key', type=str, help='AWS secret key for S3', required=True)
parser.add_argument('--s3_bucket', type=str, help = 'S3 bucket to use', default = "bg-train-input")
parser.add_argument('--dest_folder', type=str, help = 'destination folder', default = "")

parser.add_argument('--where', type=str, help = 'where clause, including "WHERE"', default = "")
parser.add_argument('--orderby', type=str, help = 'order clause including "ORDER BY"', default = "")
parser.add_argument('--timestamp_as_epoch', action="store_true", help = "If set, then dates are saved in Epoch millis",
                    default = False)
parser.add_argument('--no_column_groups', action="store_true",
                    help = "If set, then no computation of group info is done")
parser.add_argument('--columns', default = None)
args = parser.parse_args()


src_conn_factory = db_utils.ConnectionFactory(args.src_url)
cur = src_conn_factory.get_connection().cursor()
table_info = schema_info.TableInfo(args.schema, args.table)
if args.where:
    where = "WHERE %s" % args.where
else:
    where = ""
included_columns = None
if args.columns:
    included_columns = args.columns.split(',')
    columns = [""] * len(included_columns)
else:
    columns = []

table_info = db_utils.compute_table_info(src_conn_factory, table_info, where, no_groups=args.no_column_groups, force_required_columns=False,
                                         included_columns = included_columns)

print("table_info: %s" % table_info)
for column in table_info.columns:
    column_value = '"%s"' % column.name
    if args.timestamp_as_epoch and "timestamp" in column.datatype:
        column_value = "(EXTRACT(EPOCH FROM %s))" % column_value
    elif "char" in column.datatype:
        column_value = "TRANSLATE(%s, '\\r\\n', '  ')" % column_value

    if included_columns:
        if column.name in included_columns:
            columns[included_columns.index(column.name)] = column.name
    else:
        columns.append(column_value)

select = "select %s from %s.%s %s %s" % (", ".join(columns), args.schema, args.table, where, args.orderby)

manifest = db_utils.copy_to_s3_from_redshift_by_bucket(
    cur, select, table_info, args.s3_bucket, args.s3_secret_key, table_info.full_name, args.dest_folder)
local_pickle = io.StringIO()

pickle.dump(table_info, local_pickle)

session = boto3.Session(
    aws_access_key_id=args.s3_key_id,
    aws_secret_access_key=args.s3_secret_key,
)
s3 = session.client('s3')
s3_key = "%s.pickle" % (manifest[0:manifest.find("manifest")])
local_pickle.seek(0)
s3.put_object(Bucket = args.s3_bucket, Key = s3_key, Body = local_pickle)

print("Created manifest: %s" % manifest)
