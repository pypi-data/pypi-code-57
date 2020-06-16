# This compiles & loads Cython (pyx) modules if the code is more recent than .so
import pyximport

pyximport.install()

import itertools
import numpy
import math
import os.path
import bytegain.custom.model_data.feature_analysis as feature_analysis
import bytegain.custom.model_data.read_from_db as read_from_db
import bytegain.custom.nn_tools.xgb_classifier as xgb
import bytegain.custom.nn_tools.model_utils as model_utils
from bytegain.custom.model_data.row_handler import RowHandler
from bytegain.custom.model_data.bucket import ValueBucket
from bytegain.custom.model_data.extractor import RowExtractor


class SearchIdExtractor(object):
    def __init__(self):
        self._user_id_index = None
        self._user_order_index = None
        self._search_category_index = None

    def extract(self, row):
        if self._user_id_index is not None:
            search_category = row[self._search_category_index]
            if search_category is None or "_" in search_category:
                search_category = "NA"
            return "%s_%s_%s" % (row[self._user_id_index], search_category, row[self._user_order_index])
        else:
            return "%s_%s_%s" % (row['user_id'], row['search_category'], row['user_order'])

    def get_fields(self):
        return ['user_id', 'user_order', 'search_category']

    def update_fields_by_id(self, cursor_header):
        self._user_id_index = cursor_header.index('user_id')
        self._user_order_index = cursor_header.index('user_order')
        self._search_category_index = cursor_header.index('search_category')


class InterestStateExtractor(RowExtractor):
    def __init__(self):
        super(InterestStateExtractor, self).__init__("final_interest_state")

    def update_fields_by_id(self, cursor_header):
        super(InterestStateExtractor, self).update_fields_by_id(cursor_header)

    def extract(self, row):
        state = super(InterestStateExtractor, self).extract(row)
        return state in ('visit_interest', 'strong_interest', 'mild_interest')

    def get_fields(self):
        return ['final_interest_state']


class NotificationAndInterestStateExtractor(RowExtractor):
    def __init__(self):
        super(NotificationAndInterestStateExtractor, self).__init__("final_interest_state")
        self._leased_extractor = RowExtractor("notified_at")

    def update_fields_by_id(self, cursor_header):
        super(NotificationAndInterestStateExtractor, self).update_fields_by_id(cursor_header)
        self._leased_extractor.update_fields_by_id(cursor_header)

    def extract(self, row):
        state = super(NotificationAndInterestStateExtractor, self).extract(row)
        notified_at = self._leased_extractor.extract(row)
        if notified_at:
            return 3
        if state in ('visit_interest', 'strong_interest'):
            return 2
        elif state == 'mild_interest':
            return 1
        else:
            return 0

    def get_fields(self):
        return ['final_interest_state', "notified_at"]


def run_feature_analysis(filename):
    data_info = feature_analysis.DataInfo(get_selector())
    features = feature_analysis.process_features(data_info)
    feature_analysis.save_features(filename, features)
    return features


def get_dataset(feature_file, filter, label_extractor, run_analysis=False, random_seed=358377213, rows = None):
    if run_analysis:
        features = run_feature_analysis(feature_file)
        print("Features: %s" % features)
    else:
        features = feature_analysis.read_features(feature_file)
    rh = create_row_handler(features, filter, label_extractor)
    datasets = create_datasets_from_row_handler(rh, test_fraction=0.2, random_seed=random_seed, rows=rows)
    return rh, datasets


def get_selector():
    return read_from_db.Selector("apartmentlist.search_training",
                                 # None,
                                 "interest_created_at > timestamp '2017-08-15'",
                                 # "final_interest_state = 'strong_interest'",
                                 "(final_interest_state in  ('visit_interest', 'strong_interest', 'mild_interest'))",
                                 # "(final_interest_state in  ('visit_interest', 'strong_interest'))",
                                 "md5(user_id)")

def create_datasets_from_row_handler(row_handler, random_seed=83243312, test_fraction=0.2, rows=None):
    selector = get_selector()
    numpy.random.seed(random_seed)
    read_from_db.generate_row_handler_stats(selector, row_handler)
    return read_from_db.create_datasets(selector, row_handler, test_fraction, rows, shuffle_rows = False)


def compute_NGDC(results, for_model = True, by_category = False, print_users = 0):
    # First sort by ranking_key, then sort by user_id

    if for_model:
        if by_category:
            results.sort(key=lambda val: ("%s_%5.5f" % (val['id'].split("_")[1], val['prob'])), reverse = True)
        else:
            results.sort(key=lambda val: val['prob'], reverse = True)
    else:
        if by_category:
            results.sort(key=lambda val: ("%s_%04d" % (val['id'].split("_")[1], int(val['id'].split("_")[2]))))
        else:
            results.sort(key=lambda val: int(val['id'].split("_")[2]))

    results.sort(key=lambda val: int(val['id'].split("_")[0]))

    users = 0
    nDCG_sum = 0

    for u, user_rows in itertools.groupby(results, key = lambda val: val['id'].rsplit("_", 1 if by_category else 2)[0]):
        pos_count = 0
        rows = []
        row_count = 0
        iDGC = 0.0
        dgc = 0.0
        r1_rows = []
        for i, row in enumerate(r1_rows):
            row_count += 1
            rows.append(row)
            if row['pos'] > 0:
                pos_count += 1
                iDGC += 1 / (math.log(float(pos_count + 1), 2))
                dgc +=  1 / (math.log(float(i + 2), 2))
            # if i == 9:
            #     break

        if pos_count > 0 and row_count > 5 and pos_count != row_count:
        # if pos_count > 0:
            users += 1
            nDCG_sum += (dgc / iDGC)
            if users < print_users:
                for row in rows:
                    print(row)
                print("nDGC: %6.4f\n\n" % (dgc / iDGC))

    print("%d users. Avg nGDC: %5.3f" % (users, nDCG_sum / users))


def compute_groups(dataset):
    groups = []
    count = 0
    last = dataset._ids[0].split("_")[0]
    for label in dataset._ids:
        group_id = label.split("_")[0]
        if last == group_id:
            count += 1
        else:
            groups.append(count)
            last = group_id
            count = 1
    groups.append(count)

    return groups

def explode_results(results_grouped):
    output_results = []
    for group in results_grouped:
        for entry in group:
            output_results.append(entry)

    return output_results

def compute_NGDC_ranked(results, for_model = True, print_users = 0):
    users = 0
    nDCG_sum = 0
    for group in results:
        pos_count = 0
        iDGC = 0
        dgc = 0

        r1_rows = []
        for row in group:
            if "R1" in row['id']:
                r1_rows.append(row)
        group = r1_rows

        if for_model:
            group.sort(key=lambda val: val['prob'], reverse = True)
        else:
            group.sort(key=lambda val: int(val['id'].split("_")[2]))
        for i, row in enumerate(group):
            if row['pos'] > 0.0:
                iDGC += (2**row['pos'] - 1) / (math.log(float(pos_count + 2), 2))
                dgc +=  (2**row['pos'] - 1) / (math.log(float(i + 2), 2))
                pos_count += 1
                # if i == 9:
                #     break

        if pos_count > 0:
            users += 1
            nDCG_sum += (dgc / iDGC)
            if users < print_users:
                if for_model:
                    group_al = sorted(group, key=lambda val: int(val['id'].split("_")[2]))
                    for row, row_al in zip(group, group_al):
                        print("%5.3f %2d | %2d" % (row['prob'], row['pos'], row_al['pos']))

                print("nDGC: %6.4f\n\n" % (dgc / iDGC))

    print("%d users. Avg nGDC: %5.3f" % (users, nDCG_sum / users))


def compute_likes_at(results, for_model = True, by_category = False, stop_at_index = 20, print_users = 0):
    if for_model:
        if by_category:
            results.sort(key=lambda val: ("%s_%5.5f" % (val['id'].split("_")[1], val['prob'])), reverse = True)
        else:
            results.sort(key=lambda val: val['prob'], reverse = True)
    else:
        if by_category:
            results.sort(key=lambda val: ("%s_%04d" % (val['id'].split("_")[1], int(val['id'].split("_")[2]))))
        else:
            results.sort(key=lambda val: int(val['id'].split("_")[2]))

    results.sort(key=lambda val: int(val['id'].split("_")[0]))

    users = 0
    pos_sum = 0

    for u, user_rows in itertools.groupby(results, key = lambda val: val['id'].rsplit("_", 1 if by_category else 2)[0]):
        has_non_E = False
        pos_count = 0
        rows = []
        row_count = 0
        for i, row in enumerate(user_rows):
            if "E" not in row['id'].split("_")[1]:
                has_non_E = True
            row_count +=1
            rows.append(row)
            if i < stop_at_index:
                if row['pos'] == 1.0:
                    pos_count += 1

            if i >= stop_at_index and (by_category or has_non_E):
                users += 1
                pos_sum += pos_count
                break

    if pos_count > 0 and row_count > 5 and pos_count != row_count:
            if users < print_users:
                for row in rows:
                    print(row)

    print("%d users. Avg pos_sum: %5.3f" % (users, float(pos_sum) / users))

"""
Creates a RowHandler for parsing AL data and handing to XGBoost.
"""
def create_row_handler(features, filter, label_extractor, load_from=None):
    # Set this to experiment with weighting.
    weight_extractor = None
    row_handler = RowHandler(
        label_bucket=ValueBucket("positive_interest", label_extractor, has_null=False),
        id_extractor=SearchIdExtractor(),
        weight_extractor=weight_extractor,
        load_from=load_from,
        extra_fields=[])
    if load_from is None:
        # print "Excluded features: %s" % str(EXCLUDED_FEATURES)
        buckets = filter.create_buckets(features)
        for bucket in buckets:
            row_handler.add_bucket(bucket)

    return row_handler

def train_and_push(feature_json, model_name, feature_filter, group_function = None, 
    label_extractor = InterestStateExtractor(),  **train_kwrd):
    rh, datasets = get_dataset(feature_json, feature_filter, label_extractor, run_analysis=False, rows=None)
    classifier = xgb.XgbClassifier(group_function = group_function)
    classifier.train(datasets, **train_kwrd)
    results = classifier.get_sorted_results(datasets.test)
    if group_function is not None:
        results = explode_results(results)
    spec = model_utils.XgbModelSpec(model_name, ".")
    spec.save(classifier, datasets._row_handler, results)
    model_utils.save_results_as_csv(model_name + '.csv', 'id', 'pred', results)
    spec.upload(os.path.join(model_utils.GCS_BUCKET, model_name))
