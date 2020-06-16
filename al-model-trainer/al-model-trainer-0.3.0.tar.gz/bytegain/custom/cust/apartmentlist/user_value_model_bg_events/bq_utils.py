from google.cloud import bigquery
from bytegain.custom.model_data.schema_from_TableInfo import get_schema


TYPE_MAP = {'timestamp without time zone': 'TIMESTAMP',
            'character varying(256)': 'STRING'}


def if_table_exists(client, table_ref):
    from google.cloud.exceptions import NotFound
    try:
        client.get_table(table_ref)
        return True
    except NotFound:
        return False


def create_table(project, dataset_id, table_id, source_uris, schema_file_uri,
                 column_map, source_format='CSV', delimiter='|'):
    """
    Creates `table_id` in `dataset_id` without `project` from files `source_uris` using table_info file
    located at `schema_file_uri`.

    :param (str) project: GCS project
    :param (str) dataset_id: Dataset in `project`
    :param (str) table_id: Table in dataset `dataset_id`
    :param (str) source_uris: GCS path to files that will be exported into `table_id`
    :param (str) schema_file_uri: TableInfo file used to extract schema for the table
    :param (str) source_format: Source format, e.g. 'CSV'
    :param (str) delimiter: Delimiter, e.g. '|'
    :param (dict[str, dict]) column_map:
    """
    client = bigquery.Client(project=project)

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    # Try to delete the table
    if if_table_exists(client, table_ref):
        client.delete_table(table_ref)
        print("Deleted table '{}'.".format(table_id))

    # Load TableInfo
    table_info = get_schema(schema_file_uri, subdirs={'all': ''}).get('all')
    assert table_info, "Table info not found"

    # Set schema from table_info
    schema = []
    for col in table_info.columns:
        col_name = col.name
        col_type = col.datatype
        # Map types
        col_type = TYPE_MAP.get(col_type, col_type)
        col_map = column_map.get(col_name)
        # Map names and types if needs to be converted
        if col_map:
            field_name = col_map.get('name', col_name)
            field_type = col_map.get('type', col_type)
        else:
            field_name = col_name
            field_type = col_type
        schema.append(bigquery.SchemaField(field_name, field_type))

    job_config = bigquery.LoadJobConfig()
    job_config.schema = schema
    job_config.field_delimiter = delimiter

    format = None
    for allowed_format in vars(bigquery.SourceFormat):
        if source_format==allowed_format:
            format = source_format
    assert format, "'%s' is not allowed format" % source_format

    job_config.source_format = format
    load_job = client.load_table_from_uri(
        source_uris, table_ref, job_config=job_config
    )  # API request
    print("Starting job {}".format(load_job.job_id))

    load_job.result()  # Waits for table load to complete.
    print("Job finished.")

    destination_table = client.get_table(table_ref)
    print("Loaded {} rows.".format(destination_table.num_rows))
