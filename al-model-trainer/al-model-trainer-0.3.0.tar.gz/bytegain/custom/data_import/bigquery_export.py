import argparse
import os
import subprocess
import time
import uuid
from sys import stdout

from google.cloud import bigquery

client = bigquery.Client()


def async_query(query):
    print('\n>>> Running async query ...')

    job = client.run_async_query(uuid.uuid4().hex, query)
    job.use_legacy_sql = False
    job.use_query_cache = True

    job.result()  # Wait for job to complete.

    if job.error_result or job.errors:
        print('\n!!! Query job finished with errors:\n', job.error_result, '\n', job.errors)
        exit(1)

    print('Query returned %d rows.' % job.query_results().total_rows)

    job.destination.reload()

    return job.destination


def export_table(table, gcs_pattern):
    print('\n>>> Extracting table to GCS ...')
    job = client.extract_table_to_storage(uuid.uuid4().hex, table, gcs_pattern)
    job.destination_format = 'NEWLINE_DELIMITED_JSON'
    job.compression = 'GZIP'

    job.begin()

    # Wait for job to complete
    retry_count = 100
    interval = 3  # seconds
    stdout.write('Waiting for job to complete ')
    while retry_count > 0 and job.state != 'DONE':
        retry_count -= 1
        stdout.write('.')
        stdout.flush()
        time.sleep(interval)
        job.reload()

        if job.error_result or job.errors:
            print('\n\n!!! Extract job finished with errors:\n', job.error_result, '\n', job.errors)
            exit(1)
    if retry_count == 0:
        print('\n\n!!! Extract job taking too long. Bailing. The job may eventually complete, you\'re on your own!\n')
        exit(1)
    print('.. DONE')


def gcs_cleanup(gcs_pattern):
    print('\n>>> Cleaning up GCS %s ...' % gcs_pattern)
    try:
        # quick and dirty gsutil call so we don't have to implement it all using the low level storage lib
        print(subprocess.check_output(['gsutil', '-m', 'rm', gcs_pattern], stderr=subprocess.STDOUT))
    except subprocess.CalledProcessError as cpe:
        if '1 files/objects could not be removed' in cpe.output:
            # try again without the -m flag due to some weirdness in gsutil
            try:
                print(subprocess.check_output(['gsutil', 'rm', gcs_pattern], stderr=subprocess.STDOUT))
            except subprocess.CalledProcessError as cpe2:
                if 'No URLs matched' not in cpe2.output:
                    print(cpe2.output)
                    raise cpe2
        else:
            print(cpe.output)
            raise cpe


def local_copy(gcs_pattern, local_dir):
    print('\n>>> Copying from GCS to local ...')
    # quick and dirty gsutil call so we don't have to implement it all using the low level storage lib
    print(subprocess.check_output(['gsutil', '-m', 'cp', gcs_pattern, local_dir], stderr=subprocess.STDOUT))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Export the results of a BigQuery query to GCS and optionally copy the files locally.')
    parser.add_argument('query',
                        help='the query to run. For complex queries use a file as input and pass "$(<query_file)", including the quotes.')
    parser.add_argument('gcs_prefix', help='the GCS URL prefix, e.g. "gs://bucket/dir/prefix"')
    parser.add_argument('--local-copy', dest='dir',
                        help='make a local copy in the target directory (will try to mkdir if it doesn\'t exist)')
    args = parser.parse_args()
    print('Query:\n%s' % args.query)
    print('GCS prefix: %s' % args.gcs_prefix)
    if not args.gcs_prefix.startswith('gs://'):
        print('!!! gcs_prefix must start with gs://')
        exit(1)
    local_dir = args.dir
    if local_dir:
        local_dir = os.path.abspath(local_dir)
        print('Local dir: %s' % local_dir)
        if os.path.exists(local_dir):
            if not os.path.isdir(local_dir):
                print('!!! local path exists but it is not a directory')
                exit(1)
        else:
            os.makedirs(local_dir, mode=0o755)

    temp_table = async_query(args.query)
    gcs_pattern = args.gcs_prefix + '-*.jsonl.gz'
    gcs_cleanup(gcs_pattern)
    export_table(temp_table, gcs_pattern)
    if local_dir:
        local_copy(gcs_pattern, local_dir)
