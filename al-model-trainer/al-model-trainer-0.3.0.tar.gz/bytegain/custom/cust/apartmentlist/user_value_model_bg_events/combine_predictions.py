import csv
from bytegain.zap.utils import gcs
import logging
from google.cloud import storage
import tempfile
import json
import dateutil.parser as dt_parser

logger = logging.getLogger('combine_al_predictions')


def run(driver_input, map_config, stages, dataflow_args, input_predictions, output_predictions, tmp_dir):
    """
    Reads AL BG user value model predictions, which are obtained via running driver in predict mode, and
    generates csv with columns (userId,signup_timestamp,prediction,current_lease_status)
    and another csv with columns (date,sum_predictions,average_prediction)
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
        logging.info("File downloaded: %s" % local_path)
        blob.download_to_filename(local_path)
        local_files.append(local_path)

    # Get users and probabilities
    users = []
    for local_file in local_files:
        with open(local_file, 'r') as input_file:
            logging.info("File opened: %s" % local_file)
            for row in input_file:
                row_json = json.loads(row)
                user_id, signup_timestamp = row_json['id'].split('_')
                prediction = row_json['probability'][0]
                label = row_json['label']
                users.append((user_id, signup_timestamp, prediction, label))

    assert len(users) > 0

    # Sort by signup timestamp
    logger.info("Sorting by signup timestamp")
    users = sorted(users, key=lambda user: user[1])

    logger.info("Read %d users" % len(users))

    def extract_date(timestamp):
        return dt_parser.parse(timestamp)

    def extract_day(timestamp):
        return timestamp[8:10]

    # Go through sorted users and generate daily stats
    logger.info("Generating stats")
    stats = []
    preds_sum = 0.0
    user_count = 0
    prev_day = extract_day(users[0][1])
    for user in users:
        cur_day = extract_day(user[1])
        if cur_day != prev_day:
            date = user[1][:10]
            aver_pred = preds_sum / user_count
            logging.info('Sum of predictions: %.4f' % preds_sum)
            logging.info('Average prediction: %.4f' % aver_pred)
            stats.append((date, preds_sum, aver_pred))
            preds_sum = 0.0
            user_count = 0
        preds_sum += float(user[2])
        user_count += 1
        prev_day = cur_day

    start_date = stages['sessions']['data_start_date']
    end_date = stages['sessions']['data_end_date']

    predictions_output_filename = 'AL_user_value_predictions_%s_%s.csv' % (start_date, end_date)
    predictions_output_file = local_tmp_dir + predictions_output_filename

    with open(predictions_output_file, "w") as o_file:
        writer = csv.writer(o_file)
        writer.writerow(["userId", "signup_timestamp", "prediction", "current_lease_status"])
        writer.writerows(users)

    logger.info("Local file with predictions: %s" % predictions_output_file)

    stats_output_filename = 'AL_user_value_stats_%s_%s.csv' % (start_date, end_date)
    stats_output_file = local_tmp_dir + stats_output_filename

    with open(stats_output_file, "w") as o_file:
        writer = csv.writer(o_file)
        writer.writerow(["date", "sum_predictions", "average_prediction"])
        writer.writerows(stats)

    logger.info("Local file with stats: %s" % stats_output_file)

    logger.info("Cloud output dir: %s" % output_predictions)

    gcs.upload_local_files(
        local_file_paths=[predictions_output_file, stats_output_file],
        gs_path=output_predictions
    )

    logger.info("Cloud output dir: %s" % output_predictions)

    return {'n_users': len(users)}
