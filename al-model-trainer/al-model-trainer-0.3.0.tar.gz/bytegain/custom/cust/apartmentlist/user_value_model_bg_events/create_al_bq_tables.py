from bytegain.custom.cust.apartmentlist.user_value_model_bg_events.bq_utils import create_table
import argparse


def get_import_files(source_uri, schema, table_id):
    prefix = '%s/%s_%s/%s.%s.' % (source_uri, schema, table_id, schema, table_id)
    files = '%s*_part_00.gz' % prefix
    schema_file = '%s.pickle' % prefix
    return (files, schema_file)


if __name__=='__main__':
    parser = argparse.ArgumentParser("Creates (or overwrites) AL BQ tables from external data")
    parser.add_argument('--source_uri', required=True, help='GCS location of external files, '
                                                            'e.g. gs://bg-al-ltv-data/2018-10-01--2019-05-01/')
    args = parser.parse_args()

    project = 'bg-event-ingester'
    dataset_id = 'al'

    column_map = {'user_id': {'name': 'userId', 'type': 'STRING'},
                  'created_at': {'name': 'timestamp'}}


    def create_al_bq_table(schema, table_id):
        source_uris, schema_file = get_import_files(args.source_uri, schema, table_id)
        create_table(project=project, dataset_id=dataset_id, table_id=table_id,
                     source_uris=source_uris, schema_file_uri=schema_file, column_map=column_map)

    # Table with leases
    create_al_bq_table('etl', 'acappella_leases')
    # Sign up data
    create_al_bq_table('web', 'modals')