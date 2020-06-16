import argparse
from datetime import datetime, timedelta

from google.cloud import storage

import bytegain.custom.model_data.feature_analysis as model_fa
from . import feature_analysis
from .compare_features import compare_features


def features_filename(features_type, date_str):
    return '%s/%s-features-%s.json' % (date_str, features_type, date_str.replace('/', '-'))


def date_str(d):
    return d.strftime("%Y/%m/%d")


parser = argparse.ArgumentParser(description='Analyze features from AL request logs and optionally notify.')
parser.add_argument('--type', help='Type of features: lease, search_rank',
                    choices=[feature_analysis.TYPE_LEASE, feature_analysis.TYPE_SEARCH_RANK], required=True)
args = parser.parse_args()

gcs_client = storage.Client(project='bg-rest-api')
bucket = gcs_client.lookup_bucket('al-log-analysis')

today = date_str(datetime.now())

print('Running feature analysis for requests from %s (UTC)' % today)
where = "_PARTITIONTIME = TIMESTAMP('%s')" % today.replace('/', '-')
if today == date_str(datetime.utcnow()):
    where = '(' + where + ' OR _PARTITIONTIME IS NULL)'
stats_runner = feature_analysis.StatsRunner(feature_analysis.rows_from_bq_query(args.type, where))
current_features = stats_runner.run()
current_features_json = model_fa.features_to_json(current_features)

current_blob = bucket.blob(features_filename(args.type, today))
print('Uploading current features to: gs://%s/%s' % (current_blob.bucket.name, current_blob.name))
current_blob.upload_from_string(current_features_json, content_type='application/json')

previous_feature_analysis_json = None
previous_blob = None
previous_date = None
# Go back 10 days and try and find something if yesterday's run failed to produce a file.
for i in range(10):
    previous_date = date_str(datetime.now() - timedelta(days=i + 1))
    previous_blob = bucket.get_blob(features_filename(args.type, previous_date))
    if previous_blob:
        previous_feature_analysis_json = previous_blob.download_as_string()
        break

if not previous_feature_analysis_json:
    raise Exception('Cannot find previous feature analysis file in GCS')

print('Previous features: gs://%s/%s' % (previous_blob.bucket.name, previous_blob.name))

previous_features = model_fa.features_from_json(previous_feature_analysis_json)

if compare_features(current_features, today, previous_features, previous_date):
    exit(1)
