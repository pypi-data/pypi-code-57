import argparse
import os
from collections import defaultdict
import time
from bytegain.custom.data_import.clone_redshift_table import TableCloner
from bytegain.custom.data_import.schema_info import read_schema_from_file, save_schema, TableInfo, ColumnInfo

import bytegain.data_import.segment_utils as segment_utils
import bytegain.custom.data_import.db_utils as db_utils

def comma_list(s):
    if s:
        return s.split(",")
    return None

def create_joined_table(cur, table_info, select, sortkey):
    cur.execute("drop table if exists %s" % table_info.full_name)

    statement = "create table %s distkey(%s) sortkey(%s) as (%s)" % (
            table_info.full_name, sortkey, sortkey, select)
    print(statement)
    cur.execute(statement)

def get_join_select(schema_info, dst_schema, output_table, where):
    """ Creates a join select statement.  Returns select statement and
    a TableInfo representing the output of the Select.
    """
    start_time = time.time()
    columns = []
    src_columns = defaultdict(list)
    src_columns_table = defaultdict(list)
    src_columns_datatype = defaultdict(list)
    main_table = schema_info.main_table
    src_schema = schema_info.schema
    out_table_info = TableInfo(dst_schema, output_table)

    for column in main_table.columns:
        out_table_info.add_column(ColumnInfo(column.name, column.datatype))
        columns.append("%s.%s.%s\n" % (src_schema, main_table.table, column.name))

    for src_table in list(schema_info.join_tables.values()):
        for column in src_table.columns:
            if not main_table.has_column(column.name):
                src_columns[column.name].append(column)
                src_columns_table[column.name].append(src_table.table)
                src_columns_datatype[column.name].append(column.datatype)

    for columnname in src_columns:
        tables = src_columns_table[columnname]
        if len(tables) == 1:
            out_table_info.add_column(ColumnInfo(columnname, src_columns[columnname][0].datatype))
            columns.append("%s.%s" % (tables[0], columnname))
        else:
            any_char = False
            datatypes = src_columns_datatype[columnname]
            datatype = datatypes[0]
            # Char len varies, but ignore that
            all_same = all(x==datatypes[0] for x in datatypes) or all('char' in x for x in datatypes)
            if not all_same:
                print("Some varying datatypes for %s: %s" % (columnname, str(datatypes)))
                any_char = any('char' in x for x in datatypes)
                any_bool = any('bool' in x for x in datatypes)
            case = "case "
            for table, datatype in zip(tables, datatypes):
                value = "%s.%s" % (table, columnname)
                if not all_same:
                    if any_char:
                        if 'char' not in datatype:
                            # convert to char
                            print("Converting %s to char" % value)
                            if 'bool' in datatype:
                                #Cannot convert bool directly to char
                                value = "%s::int::char" % value
                            else:
                                value = "%s::char" % value
                            datatype = "varchar"
                    elif any_bool:
                        if 'bool' in datatype:
                            print("Converting %s to int" % value)
                            value = "%s::int" % value
                            datatype = "int"
                case += "\twhen %s.%s is not null then %s \n" % (table, columnname, value)
            case += "\telse NULL end as %s\n" % columnname
            columns.append(case)
            out_table_info.add_column(ColumnInfo(columnname, datatype))

    if len(out_table_info.columns) != len (columns):
        raise Exception("New table has wrong number of columns: %s != %s" % (str(out_table_info), columns))

    from_clause = "%s.%s\n" % (src_schema, main_table.table)
    for table in schema_info.join_tables:
        # AL uses user_id as distkey and received_at as sortkey
        from_clause += "left outer join %s.%s using (id)\n" % (src_schema, table)

    select = "select %s from %s %s" % (",".join(columns), from_clause, where)
    return select, out_table_info

parser = argparse.ArgumentParser(description='Copies segment data from a segment redshift warehouse to BG redshift')
parser.add_argument('--src_url', type=str, help='segment db url', required=True)
parser.add_argument('--dst_url', type=str, help = 'Bytegain redshift DB URL', required = True)
parser.add_argument('--schema_desc', type = str, help = 'Filename of schema description', required = True)
parser.add_argument('--dst_schema', type = str, help = 'BG customer name', required = True)
parser.add_argument('--src_region', type = str, help = 'SRC AWS region', default = "us-east-1")
parser.add_argument('--start_date', type = segment_utils.valid_date, help = 'Start date of data to copy', default = None)
parser.add_argument('--end_date', type = segment_utils.valid_date, help = 'End date of data to copy', default = None)
parser.add_argument('--s3_key_id', type=str, default = "AKIAIGHWWWWWV534ALTA",
                    help='AWS user id for S3', required=True)
parser.add_argument('--s3_secret_key', type=str, default = os.environ.get("S3_SECRET_KEY"),
                    help='AWS secret key for S3', required=True)
parser.add_argument('--sortcolumn', type=str, default = "user_id", help = "Sort/dist column for created table")
parser.add_argument('--skip_existing', type=bool, default = False, help = "If true, then skip tables that already exist in DST")
parser.add_argument('--incremental', action="store_true", default = False, help = "If set, then incrementally loads data into tables")
parser.add_argument('--output_table', type=str, default=None, help = "Name of output table to create/add to")
parser.add_argument('--where', type=str, help = 'additional where clause', default = None)
parser.add_argument('--s3_only', action="store_true", default = False, help = 'If set, then data is only copied to S3')
parser.add_argument('--gzip', action="store_true", default = False, help = 'If set, then s3 data is GZIP')
parser.add_argument('--s3_prefix', type=str, default = None, help = "S3 Destination directory for data load")

args = parser.parse_args()

# Create Where clause from start/end dates
where = db_utils.create_date_clause(args.start_date, args.end_date)
schema_info = read_schema_from_file(args.schema_desc)

# Clone the main tracks table
src_conn_factory = db_utils.ConnectionFactory(args.src_url)
dst_conn_factory = db_utils.ConnectionFactory(args.dst_url)
events = [g[0] for g in schema_info.main_table.get_column('event')._groups]
if len(events) > 0:
    tracks_where = db_utils.and_where(where, "event in ('%s')" % ("' ,'".join(events)))
else:
    tracks_where = where
main_cloner = TableCloner(schema_info.main_table, tracks_where, args.dst_schema, args.src_region, args.s3_key_id, args.s3_secret_key, args.s3_prefix,
	use_tablename_column = True)
if args.s3_only:
    manifest = main_cloner.run_select_from_redshift(src_conn_factory.get_connection(), args.gzip)
else:
    main_cloner.clone_table(src_conn_factory, dst_conn_factory, main_table, "id", args.skip_existing, args.incremental)

page_cloner = TableCloner(schema_info.page_table, where, args.dst_schema, args.src_region, args.s3_key_id, args.s3_secret_key, args.s3_prefix,
	use_tablename_column = True)
if args.s3_only:
    manifest = page_cloner.run_select_from_redshift(src_conn_factory.get_connection(), args.gzip)
else:
    page_cloner.clone_table(src_conn_factory, dst_conn_factory, main_table, "id", args.skip_existing, args.incremental)

# Iterate through all tables in schema and clone them
for table in list(schema_info.join_tables.values()):
    cloner = TableCloner(table, where, args.dst_schema, args.src_region, args.s3_key_id, args.s3_secret_key, args.s3_prefix,
    	use_tablename_column = True)
    tablename =  "%s_%s" % (table.schema, table.table)
    if args.s3_only:
        manifest = cloner.run_select_from_redshift(src_conn_factory.get_connection(), args.gzip)
    else:
        success = cloner.clone_table(src_conn_factory, dst_conn_factory, tablename, "id", args.skip_existing, args.incremental)

save_schema("%s_s3" % (args.schema_desc), schema_info, compact = True)

# Join tracks & other tables into one big table
if args.output_table and not args.s3_only:
    dst_cur = dst_conn_factory.get_connection().cursor()
    dst_cur.execute("set search_path to '%s'" % args.dst_schema)
    schema_info.translate_schema_tablenames(args.dst_schema)
    where = db_utils.create_date_clause(args.start_date, args.end_date, schema_info.main_table.full_name)

    # TODO(chris): Filter down to just joined events.
    if args.where is not None:
        if len(where) >0:
            where = "%s AND %s" % (where, args.where)
        else:
            where = args.where

    if len(where) > 0:
        where = "WHERE %s" % where

    select, out_table_info = get_join_select(schema_info, args.dst_schema, args.output_table, where)
    save_schema("%s" % args.output_table, out_table_info, compact = True)
    create_joined_table(dst_cur, out_table_info, select, args.sortcolumn)
