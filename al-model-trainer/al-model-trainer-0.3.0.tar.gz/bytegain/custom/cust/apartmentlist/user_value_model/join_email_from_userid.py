import argparse
import csv
import json
import logging
import os
import tempfile

import psycopg2
from bytegain.data_import.segment_utils import valid_date
from bytegain.zap.utils import gcs
from google.cloud import storage

logger = logging.getLogger('join_email_from_userid')


def create_connection(dburl=None):
    if dburl is None:
        dburl = os.environ['AL_REDSHIFT_URL']

    return psycopg2.connect(dburl)


def attach_email_to_pred(driver_input, map_config, stages, dataflow_args, input_predictions,
                         output_predictions, tmp_dir):
    """
        Outputs a new CSV which has UserId+email+LTV.
        Input is files with predictions made by cloud ml prediction service containing UserId,LTV
    """
    if not input_predictions.endswith('/'):
        input_predictions += '/'

    if not output_predictions.endswith('/'):
        output_predictions += '/'

    # Download prediction files
    bucket, gs_path = gcs.parse_gs_url(input_predictions)

    client = storage.Client()
    bucket = client.bucket(bucket)
    files = []
    blobs = bucket.list_blobs(prefix=gs_path)
    for blob in blobs:
        filename = blob.name.rsplit('/', 1)[1]
        if filename.startswith('prediction.results'):
            files.append(filename)
    local_files = []
    local_tmp_dir = tempfile.mkdtemp() + '/'
    for filename in files:
        blob = bucket.blob(gs_path + filename)
        local_path = local_tmp_dir + filename
        blob.download_to_filename(local_path)
        local_files.append(local_path)

    # Get users and probabilities
    users = []
    for local_file in local_files:
        with open(local_file, 'r') as input_file:
            for row in input_file:
                row_json = json.loads(row)
                user_id = row_json['id'].rsplit('_', 2)[0]
                prediction = row_json['probability'][0]
                users.append((user_id, prediction))
    users = sorted(users, key=lambda user: user[1], reverse=True)

    logger.info("Read %d users" % len(users))

    assert len(users) > 0

    # Select only users with emails
    start_date = stages['sessions']['data_start_date']

    select = """select user_id, email from api.identifies
    where email is not null and received_at > timestamp '%s'
    order by received_at desc""" % start_date

    emails = {}

    with create_connection() as connection:
        connection.autocommit = False
        with connection.cursor() as cursor:
            cursor.itersize = 100000
            print("Statement: %s" % select)
            cursor.execute(select)
            cursor.fetchone()
            for row in cursor:
                user_id = row[0]
                email = row[1]
                if not user_id in emails:
                    emails[user_id] = email
    logger.info("Read %d users" % len(users))
    output_count = 0

    end_date = stages['sessions']['data_end_date']
    output_filename = 'AL_user_value_predictions_%s-%s_with_emails.csv' % (start_date, end_date)
    output_file = local_tmp_dir + output_filename

    with open(output_file, "w") as o_file:
        writer = csv.writer(o_file)
        for user, ltv in users:
            if user in emails:
                output_count += 1
                writer.writerow([user, emails[user], "%6.4f" % float(ltv)])

    logger.info("Local output file: %s" % output_file)
    logger.info("Cloud output dir: %s" % output_predictions)

    gcs.upload_local_files(local_file_paths=output_file, gs_path=output_predictions)

    gs_output_file = output_predictions + output_filename
    logger.info("Cloud output file: %s" % gs_output_file)

    if output_count < len(users):
        logger.warn("%d of %d users not found" % (len(users) - output_count, len(users)))
    return {'n_users': len(users), 'output_file': gs_output_file}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, required=True, help='GCS path to predictions made by CloudML')
    parser.add_argument('--output', type=str, help='Output csv')
    parser.add_argument('--start_date', type=valid_date, help='Start data date')

    args = parser.parse_args()
    stages = {"data_start_date": args.start_date}  # FIXME(yuri): this doesn't look right
    attach_email_to_pred(None, None, stages=stages, dataflow_args=None,
                         input_predictions=args.input, output_predictions='', tmp_dir='/tmp/asa')
