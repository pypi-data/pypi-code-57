import argparse
import json
import importlib

from google.cloud import bigquery

import bytegain.custom.cust.apartmentlist.al_xgb as al_xgb
import bytegain.custom.model_data.read_from_db as read_from_db
import bytegain.custom.nn_tools.model_utils as model_utils
from bytegain.custom.model_data.extractor import RowExtractor
from bytegain.custom.nn_tools.prod_classifier import ProdXgbClassifier

parser = argparse.ArgumentParser(description='Tests a model against BQ logs data')
parser.add_argument('--count', type=int, default=1000, help='# examples to verify')
parser.add_argument('--date', type=str, required=True)
parser.add_argument('--model_config', type=str, help = "python var with model config")
parser.add_argument('--source_model', type=str, default = None, help = "Model for source rows, if none use model_config")

args = parser.parse_args()

_bq_client = bigquery.Client(project='bg-rest-api')

def get_config(model_config):
    module, var = model_config.rsplit('.', 1)
    module = importlib.import_module(module)
    return getattr(module, var)

def get_model_name(model_config):
    if args.source_model:
        return args.source_model
    else:
        return "%s_%s" % (model_config['model_name'], model_config['model_version'])

def get_input_rows(config):
    query = """SELECT
raw_score,
features
FROM
`bg-rest-api.al.service_logs`
WHERE
_PARTITIONTIME = TIMESTAMP("{partition_day}")
and model_id='{model_id}'
order by rand() limit {count}
""".format(partition_day = args.date, count=args.count, model_id=get_model_name(config))
    job_config = bigquery.QueryJobConfig()
    # print "BQ query: %s" % query
    query_job = _bq_client.query(query, job_config=job_config)  # API request - starts the query
    iterator = query_job.result()
    rows = list(iterator)
    output_rows = []
    return rows


def load_model(model_name):
    model_spec = model_utils.XgbModelSpec(model_name, path = None)
    model_spec.download(for_prod=False)
    return model_spec, ProdXgbClassifier(model_spec)


def get_local_prediction(classifier, row):
    json_dict = json.loads(row)
    return classifier.classify(json_dict)


def process_lease(input_rows):
    diff = 0
    pred_sum = 0.0
    logs_sum = 0.0
    for row in input_rows:
        prediction = get_local_prediction(classifier, row.features)
        server_prediction = row.raw_score
        pred_sum += prediction
        logs_sum += server_prediction
        delta = server_prediction - prediction
        if abs(delta) > 0.0001:
                    # print ("Delta: %20s %6.4f %6.4f : %7.5f %s" % (id, prediction, train_pred, delta, str(row)))
                    # if classifier is not None:
                    #     print ("input row: %s" % str(classifier._row_handler._row_handler.get_data_from_row(row)))
                    # print "--------------"
                    # misses.append(row)
                    # print ("%5.3f -> %5.3f (%3d%%)" % (server_prediction, prediction, prediction * 100/server_prediction - 100))
                    diff += 1

    count = len(input_rows)
    if count == 0:
        print ("No rows found!")
        exit(1)

    print("%5.3f%% same" % (100 - (diff * 100.0 / count)))
    print("Avg prediction: %6.4f (logs: %6.4f)" % (pred_sum / count, logs_sum / count))
    if count != args.count:
        print("Too few examples: %d" % count)

config = get_config(args.model_config)
model_name = "%s_%s" % (config['model_name'], config['model_version'])

model_spec, classifier = load_model(model_name)
row_handler = classifier._row_handler
input_rows = get_input_rows(config)

print ("Testing against local model")

process_lease(input_rows)

