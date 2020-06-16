import argparse
import csv
import http.client
import json
import importlib
from collections import defaultdict

import psycopg2
import psycopg2.extras

import bytegain.custom.cust.apartmentlist.al_xgb as al_xgb
# import bytegain.custom.cust.apartmentlist.search_data as search_data
import bytegain.custom.model_data.read_from_db as read_from_db
import bytegain.custom.nn_tools.model_utils as model_utils
from bytegain.custom.model_data.extractor import RowExtractor
from bytegain.custom.nn_tools.prod_classifier import ProdXgbClassifier

parser = argparse.ArgumentParser(description='Convert AL data to json')
parser.add_argument('--count', type=int, default=100, help='# examples to verify')
parser.add_argument('--server', type=str, default="localhost:5000")
parser.add_argument('--redshift_url', type=str, default=None)
parser.add_argument('--api_key', type=str, default="AL_TESTING")
parser.add_argument('--model', type=str, help="name of model to test")
parser.add_argument('--model_dir', type=str, help="model directory- if not set load from S3", default=None)
parser.add_argument('--model_config', type=str, help = "python var with model config")
parser.add_argument('--random_seed', type=int, default=9232323)
parser.add_argument('--epsilon', type=float, default=1E-5)
parser.add_argument('--local_model', type=bool, default=False, help="If set, then load model locally for testing")
parser.add_argument('--save_json', type=str, default=None,
                    help="If set, then save requests as json files instead of sending to server")

args = parser.parse_args()

user_ids = set()


def get_config(model_config):
    module, var = model_config.rsplit('.', 1)
    module = importlib.import_module(module)
    return getattr(module, var)

def get_input_rows(config, fields, sortby="random()"):
    model_name = "%s_%s" % (config['model_name'], config['model_version'])
    if "search" in model_name:
        pass
        # selector = search_data.get_selector()
        # extractor = search_data.SearchIdExtractor()
    else:
        selector = al_xgb.get_selector(config)
        extractor = RowExtractor(config['id_field'])

    statement = "select * from %s %s order by %s limit %d" % (
        selector._table, ("where %s" % selector._where) if selector._where is not None else "", sortby,
        args.count * 100)

    with read_from_db.create_connection() as connection:
        all_rows = []
        fields.extend(extractor.get_fields())
        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            cursor.execute("set seed to %f" % (1.0 / args.random_seed))
            cursor.execute(statement)
            for row in cursor:
                dict_row = {}
                for field in fields:
                    dict_row[field] = row[field]
                    if field == 'message_counts':
                        dict_row[field] = None

                all_rows.append(dict_row)

    unique_users = set()
    rows = {}
    for row in all_rows:
        id = extractor.extract(row)
        if id not in unique_users:
            if len(unique_users) == args.count * 10:
                break
            unique_users.add(id)
        rows[str(id)] = row
    return rows



def load_model(model_name):
    model_spec = model_utils.XgbModelSpec(model_name, args.model_dir)

    if args.model_dir is None:
        model_spec.download(for_prod=False)

    return model_spec, ProdXgbClassifier(model_spec)


def get_local_prediction(classifier, row):
    return classifier.classify(row)


def get_json(row):
    container = {'api_key': args.api_key, 'services': [{'service': 'model', 'models': model_name, 'data': row}]}
    return json.dumps(container, indent=4, sort_keys=True)


def get_server_prediction(connection, row):
    json_data = get_json(row)
    # print ("Post: %s" % str(json_data))
    connection.request("POST", "/apartmentlist/lease_predict", json_data)
    response = connection.getresponse()
    body = response.read()
    # print ("Response: %s" % str(json_response))
    try:
        json_response = json.loads(body)
        prediction = json_response["responses"][0]["predictions"][0]["raw_score"]
    except Exception as e:
        print("Post: %s" % str(json_data))
        print("Response: %s" % str(body))
        raise
    return prediction


def get_server_search_prediction(connection, json_data):
    # print ("Post: %s" % str(json_data))
    connection.request("POST", "/apartmentlist/search_rank", json_data)
    response = connection.getresponse()
    body = response.read()
    json_response = json.loads(body)
    # print ("Response: %s\n\n" % str(json_response))
    try:
        prediction = json_response["responses"][0]
    except Exception as e:
        print("Post: %s" % str(json_data))
        print("Response: %s" % str(json_response))
        raise
    return prediction


def get_train_predictions(ids, csv_file):
    predictions = {}
    ids = set(ids)
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        for line in reader:
            id = line[0]
            if id in ids:
                predictions[id] = float(line[1])

    print("found %d of %d" % (len(predictions), len(ids)))
    return predictions


def group_by_id(rows):
    by_id = defaultdict(lambda: [])
    for k, v in list(rows.items()):
        id = k.split("_")[0]
        by_id[id].append(v)

    return by_id


def find_row_by_order_id(train_rows, id):
    for row in train_rows:
        if int(row['id'].split("_")[2]) == id:
            return row
    return None


def process_search(db_rows, train_rows, row_handler):
    new_train_rows = {}
    for k, v in list(train_rows.items()):
        # print v
        new_train_rows[k] = {'prob': v, 'id': k}

    db_rows = group_by_id(db_rows)
    train_rows = group_by_id(new_train_rows)
    count = 0
    miss_count = 0
    rh_keys = set(row_handler.get_fields())
    rh_keys.add('unit_id')
    for id, user_db_rows in list(db_rows.items()):
        # print "Id: %s" % id
        if count == args.count:
            break
        if id in train_rows and len(user_db_rows) > 5:
            count += 1
            process_unit_rows(rh_keys, user_db_rows)
            user_train_rows = train_rows[id]
            existing_values = user_db_rows[0]
            user_keys = set(existing_values.keys())
            for row in user_db_rows:
                for k, v in list(row.items()):
                    if k in user_keys and existing_values[k] != v:
                        user_keys.remove(k)
            user_values = {}

            for k in user_keys:
                user_values[k] = existing_values[k]
                for row in user_db_rows:
                    del row[k]

            container = {'api_key': args.api_key,
                         'services': [{'service': 'search',
                                       'model': model_name,
                                       'user': user_values,
                                       'units': user_db_rows}]}

            json_data = json.dumps(container, indent=4, sort_keys=True)
            # print json_data

            prediction = get_server_search_prediction(connection, json_data)
            if len(prediction) != len(user_db_rows):
                print("Wrong number of predictions: %d != %d" % (len(prediction), len(user_db_rows)))
                print(prediction)
            miss = False
            for result in prediction:
                id = result['unit_id']
                raw_score = result['raw_score']
                train_row = find_row_by_order_id(user_train_rows, id)
                if train_row == None:
                    print("could not find row: %d in %s" % (id, user_train_rows))
                    miss = True
                else:
                    # print train_row
                    if abs(train_row['prob'] - raw_score) > 0.00001:
                        miss = True
                        print("Missed %s %f != %f" % (id, raw_score, train_row['prob']))
            if miss:
                miss_count += 1
    print("Missed: %d of %d" % (miss_count, count))


def process_unit_rows(rh_keys, user_db_rows):
    for row in user_db_rows:
        row['unit_id'] = row['user_order']
    for row in user_db_rows:
        keys = set(row.keys())
        keys.difference_update(rh_keys)
        for k in keys:
            del row[k]


def process_lease(input_rows, train_rows, row_handler):
    count = 0
    diff = 0
    misses = []
    pred_sum = 0.0
    for id in input_rows:
        if count == args.count:
            break
        if id in train_rows:
            count += 1
            row = input_rows[id]
            if args.save_json:
                print ("Saving json")
                json_data = get_json(row)
                with open(args.save_json % count, "wt") as f:
                    f.write(json_data + "\n")
            else:
                if connection:
                    prediction = get_server_prediction(connection, row)
                else:
                    prediction = get_local_prediction(classifier, row)

                train_pred = train_rows[id]
                pred_sum += prediction
                delta = train_pred - prediction
                if abs(delta) > args.epsilon:
                    # print ("Delta: %20s %6.4f %6.4f : %7.5f %s" % (id, prediction, train_pred, delta, str(row)))
                    # if classifier is not None:
                    #     print ("input row: %s" % str(classifier._row_handler._row_handler.get_data_from_row(row)))
                    # print "--------------"
                    # misses.append(row)
                    print("%5.3f -> %5.3f (%3d%%)" % (train_pred, prediction, prediction * 100/train_pred - 100))
                    diff += 1
    print("%5.3f%% same" % (100 - (diff * 100.0 / count)))
    print("Avg prediction: %6.4f" % (pred_sum /count))
    if count != args.count:
        print("Too few examples: %d" % count)
    if misses > 1:
        miss_values = defaultdict(lambda: defaultdict(lambda: 0))
        for row in misses:
            for k, v in list(row.items()):
                miss_values[k][v] = miss_values[k][v] + 1
        for k, v in list(miss_values.items()):
            print("%s: %s" % (k, str(["%s=%s" % (x, y) for x, y in list(v.items())])))

config = get_config(args.model_config)
model_name = "%s_%s" % (config['model_name'], config['model_version'])

model_spec, classifier = load_model(model_name)
# classifier._row_handler.print_summary()
# exit(0)
# model_name = 'al_finance_1.0.0'
row_handler = classifier._row_handler
input_rows = get_input_rows(config, classifier.get_fields(), "md5(user_id)" if "search" in model_name else "random()")

if args.local_model:
    print ("Testing against local model")
    row_handler.print_spec()
    connection = None
elif args.save_json is None:
    print("Testing against %s" % (args.server))
    classifier = None
    connection = http.client.HTTPSConnection(args.server)

train_rows = get_train_predictions(list(input_rows.keys()), model_spec.get_validation_file())

if "search" in model_name:
    process_search(input_rows, train_rows, row_handler)
else:
    process_lease(input_rows, train_rows, row_handler)
