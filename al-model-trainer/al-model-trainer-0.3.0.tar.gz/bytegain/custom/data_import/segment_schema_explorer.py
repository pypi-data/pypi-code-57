import argparse
import bytegain.data_import.segment_utils as segment_utils
import bytegain.custom.data_import.db_utils as db_utils
import bytegain.custom.data_import.schema_info as schema_info_module
from collections import defaultdict

def parse_where(arg):
    return arg.split(":")

parser = argparse.ArgumentParser(description='Prints data on segment schema')
parser.add_argument('--src_url', type=str, help='segment db url', required=True)
parser.add_argument('--src_schema', type = str, help = 'segment schema', required = True)
parser.add_argument('--start_date', type = segment_utils.valid_date, help = 'Start date of data to copy', default = None)
parser.add_argument('--end_date', type = segment_utils.valid_date, help = 'End date of data to copy', default = None)
parser.add_argument('--global_where', type = str, help = "Global where clause")
parser.add_argument('--where_dict', type=parse_where, nargs="+", help = "Comma separated list of table:WHERE clauses")
parser.add_argument('--out', type=str, required = True, help = "Output file for data")
parser.add_argument('--no_groups', action='store_true', help = "If set then no grouping is done")

args = parser.parse_args()

where_dict = defaultdict(lambda: None, [(x[0], x[1]) for x in args.where_dict])
where = db_utils.create_date_clause(args.start_date, args.end_date)
if len(where) > 0:
    where = "WHERE %s" % where

src_conn_factory = db_utils.ConnectionFactory(args.src_url)
tracks = schema_info_module.TableInfo(args.src_schema, "tracks", db_utils.and_where(args.global_where, where_dict["tracks"]))
tracks = db_utils.compute_table_info(src_conn_factory, tracks, where, no_groups=args.no_groups)

pages = schema_info_module.TableInfo(args.src_schema, "pages", db_utils.and_where(args.global_where, where_dict["pages"]))
pages = db_utils.compute_table_info(src_conn_factory, pages, where, no_groups=args.no_groups)

tables = db_utils.get_segment_tables(src_conn_factory, args.src_schema)
table_infos = {}
skipped_tables = []
for table in tables:
    if table == "pages":
        continue

    table_where = db_utils.and_where(args.global_where, where_dict[table])

    table_info = schema_info_module.TableInfo(args.src_schema, table, table_where)
    info = db_utils.compute_table_info(src_conn_factory, table_info, where, exclude_common = tracks, no_groups=args.no_groups)
    if not info:
        skipped_tables.append(table)
        continue
    table_infos[table] = info
    # info.print_pretty()

if skipped_tables:
    print("Skipped tables: %s" % ' '.join(skipped_tables))

schema_info = schema_info_module.SchemaInfo(args.src_schema, tracks, pages, table_infos)
schema_info_module.save_schema(args.out, schema_info, compact=True)
