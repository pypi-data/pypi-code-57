import pyximport
pyximport.install()
import os
import sys
import numpy
import importlib
import csv
import bytegain.custom.nn_tools.xgb_classifier as xgb
import bytegain.custom.nn_tools.model_utils as model_utils
import bytegain.custom.model_data.feature_analysis as feature_analysis
import bytegain.nn_tools.auc_plot as auc_plot
from bytegain.custom.nn_tools.prod_classifier import ProdXgbClassifier
from bytegain.custom.nn_tools.xgb_classifier import XgbClassifier
import bytegain.custom.model_data.read_from_db as read_from_db
from bytegain.custom.model_data.row_handler import RowHandler
from bytegain.custom.model_data.bucket import ValueBucket
from bytegain.custom.model_data.extractor import RowExtractor
from bytegain.custom.cust.apartmentlist.feature_filter import FeatureFilter




"""
import bytegain.cust.apartmentlist.al_xgb as al_xgb
import bytegain.nn_tools.model_utils as model_utils
import bytegain.nn_tools.xgb_classifier as xgb
rh, datasets = al_xgb.create_rh_and_dataset('al_handler_test.json')
results = xgb.cv(datasets, xgb.XgbClassifier, 401, parallel=True)

import bytegain.cust.apartmentlist.al_xgb as al_xgb
import bytegain.nn_tools.xgb_classifier as xgb
rh, datasets = al_xgb.create_rh_and_dataset('al_features_20161214.json')
model = xgb.XgbClassifier()
model.train(datasets)


import bytegain.nn_tools.knock_out as knock_out
import bytegain.cust.apartmentlist.leads_from_redshift as tfl
import bytegain.nn_tools.xgb_classifier as xgb

features = al_handler_from_features.read_al_features('al_handler1.json')
rh = al_handler_from_features.create_row_handler(features)
datasets = tfl.create_datasets_from_row_handler(rh, test_fraction = 0.2)
results = xgb_classifier.cv(datasets, xgb_classifier.XgbClassifier, 601)


"""

def output_feature_scores(model, rh, output):
    features = model.feature_scores(rh)

    for feature in features:
        output.write("%25s: %4.1f\n" % (feature[0], feature[1]));


def train_from_dataset(config, rh, dataset,thresholds_to_csv = True, save_predict=True):
    model = xgb.XgbClassifier(eval_metric=config['eval_metric'])
    model.train(dataset, min_child_weight=config['min_child_weight'], max_rounds=config['max_rounds'],
                max_depth=config['max_depth'], l2_norm = config['l2_norm'],l1_norm = config['l1_norm'], train_step_size = config['train_step_size'],gamma = config['gamma'],subsample=config['subsample'],scale_pos_weight=config['scale_pos_weight'],grow_policy = config["grow_policy"])
    control_results = model.get_sorted_results(dataset.get_test_control())
    model.save('lead_scoring_2.json')
    print("Control ROC_AUC: %5.3f" % auc_plot.compute_auc(control_results))
    print("Control AVG PR: %5.3f" % auc_plot.compute_avgpr(control_results))
    print("Control F_BETA: %5.3f" % auc_plot.f_beta_DLMavg(control_results, beta = 10.))

    #print(auc_plot.compute_metrics(control_results,0.005))
    #output_feature_scores(model, rh, sys.stdout)
    print('now feature importance')
    output_feature_scores(model, rh, sys.stdout)
    if save_predict:
        auc_plot.save_predictions(control_results, filename="true_and_pred.csv")
    metrics_list2 = []
    metrics_list2 = auc_plot.compute_TPFN_Thresholds(control_results, minority_class_proportion = config['minority_class_prop'], sample_size = 300000)
    if thresholds_to_csv:
        with open("new_metrics_test_fast.csv", "w", newline="") as g:
            writer = csv.writer(g)
            writer.writerows(metrics_list2)
    print("Control Revenue Voltage: $ %5.3f" % auc_plot.compute_revenue_voltage(control_results, minority_class_proportion = config['minority_class_prop'], sample_size = 300000))

    return model

def swap_from_dataset(config, rh, dataset,test_set):
    model = xgb.XgbClassifier()
    model.train(dataset, min_child_weight=config['min_child_weight'], max_rounds=config['max_rounds'],
                max_depth=config['max_depth'], l2_norm = config['l2_norm'], train_step_size = config['train_step_size'])
    control_results = model.get_sorted_results(test_set)
    print("Control AUC: %5.3f" % auc_plot.compute_auc(control_results))

    #output_feature_scores(model, rh, sys.stdout)
    return model

def output_model_summary(config, model, datasets, comments):
    features = model.feature_scores(datasets._row_handler)
    control_results = model.get_sorted_results(datasets.get_test_control())
    auc = auc_plot.compute_auc(control_results)

    with open(f"../{config['model_name']}_summary.md", "w") as fp:
        fp.write(f"## Model: {config['model_name']}\n")
        fp.write(f"* Version: {config['model_version']}\n")
        fp.write(f"* Training set: {config['table']}\n")
        fp.write(f"* Outcome: {config['outcome_field']}\n")
        fp.write(f"* Control AUC: {auc:5.3f}\n")

        fp.write("## Features\n")
        fp.write("| Feature | Weight | Description |\n")
        fp.write("|:--- |:--- |:--- |\n")
        for feature in features:
            comment = ""
            if feature[0] in comments:
                comment = comments[feature[0]]
            fp.write(f"| {feature[0]} | {feature[1]:4.1f} | {comment} |\n")
  
def test_from_dataset(config, rh, dataset,thresholds_to_csv = True):
    import pickle
    model = pickle.load(open("/Users/gabrieldurkin/dev/github.com/apartmentlist/bytegain-training/xgb_model_dump.pkl", 'rb'))
    control_results = model.get_sorted_results(dataset)
    auc_plot.plot_auc("./auc_curve.png", control_results)
    print("Control AUC: %5.3f" % auc_plot.compute_auc(control_results))
    print(auc_plot.compute_metrics(control_results))
    output_feature_scores(model, rh, sys.stdout)
    metrics_list2 = []
    metrics_list2 = auc_plot.compute_TPFN_Thresholds(control_results, minority_class_proportion = 0.0027, sample_size = 300000)
    if thresholds_to_csv:
        with open("from_file_metrics_test_fast.csv", "w", newline="") as g:
            writer = csv.writer(g)
            writer.writerows(metrics_list2)
    return model

def create_rh_and_dataset(config, testing_fraction = 0.2, shufflerows=True):
    rh = create_row_handler(config)
    datasets = create_datasets_from_row_handler(rh, config, test_fraction = testing_fraction, shufflerows = shufflerows)
    return rh, datasets

def train_and_push(config):
    model_name = config['model_name']
    if not os.path.isdir(model_name):
        print("Creating %s" % model_name)
        os.mkdir(model_name)

    rh, datasets = create_rh_and_dataset(config)
    classifier = train_from_dataset(config, rh, datasets)
    results = classifier.get_sorted_results(datasets.test)

    if not os.path.isdir(model_name):
        os.mkdir(model_name)
    os.chdir(model_name)
    model_name = "%s_%s" % (config['model_name'], config['model_version'])
    try:
        auc_plot.plot_predicted_vs_actual2('%s_p_vs_a.png' % model_name, results, points=20)
        auc_plot.plot_auc('%s_roc.png' % model_name, results)

        spec = model_utils.XgbModelSpec(model_name, ".")
        spec.save(classifier, datasets._row_handler, results)
        model_utils.save_results_as_csv(model_name + '.csv', 'id', 'pred', results)
        comments = read_from_db.feature_comments(config)
        output_model_summary(config, classifier, datasets, comments)
        spec.upload()
    finally:
        os.chdir('..')

def train_and_push_time(config, tf = 0.2):
    model_name = config['model_name']
    if not os.path.isdir(model_name):
        print("Creating %s" % model_name)
        os.mkdir(model_name)

    rh, datasets = create_rh_and_dataset(config, testing_fraction = tf, shufflerows=False)
    classifier = train_from_dataset(config, rh, datasets)
    results = classifier.get_sorted_results(datasets.test)

    if not os.path.isdir(model_name):
        os.mkdir(model_name)
    os.chdir(model_name)
    model_name = "%s_%s" % (config['model_name'], config['model_version'])
    try:
        auc_plot.plot_predicted_vs_actual2('%s_p_vs_a.png' % model_name, results, points=20)
        auc_plot.plot_auc('%s_roc.png' % model_name, results)

        spec = model_utils.XgbModelSpec(model_name, ".")
        spec.save(classifier, datasets._row_handler, results)
        #model_utils.save_results_as_csv(model_name + '.csv', 'id', 'pred', results)
        comments = read_from_db.feature_comments(config)
        output_model_summary(config, classifier, datasets, comments)
        spec.upload()
    finally:
        os.chdir('..')

def get_selector(config):
    if config['downsample']:
        where = '(%s OR CORE.public.f_bucket_number(%s, 1000) < 50)' % (config['outcome_field'], config['id_field'])
    else:
        where = None

    return read_from_db.Selector(config['table'], where,
                                 config['outcome_field'],
                                 config['id_field'],
                                 None,
                                 config.get('positive_outcome_rate_field'), config['start_date'], config['end_date'])

def get_selector_test(config):
    if config['downsample']:
        where = '(%s OR CORE.public.f_bucket_number(%s, 1000) < 50)' % (config['outcome_field'], config['id_field'])
    else:
        where = None

    return read_from_db.Selector(config['test_table'], where,
                                 config['outcome_field'],
                                 config['id_field'],
                                 None,
                                 config.get('positive_outcome_rate_field'))    

def create_datasets_from_row_handler(row_handler, config, test_fraction = 0.2, rows = None, shufflerows = True):
    selector = get_selector(config)
    numpy.random.seed(config['random_seed'])
    read_from_db.generate_row_handler_stats(selector, row_handler)
    return read_from_db.create_datasets(selector, row_handler, test_fraction, rows, shuffle_rows = shufflerows)

def create_test_data(row_handler, config, rows = None):
    selector = get_selector_test(config)
    numpy.random.seed(config['random_seed'])
    read_from_db.generate_row_handler_stats(selector, row_handler)
    return read_from_db.create_datasets(selector, row_handler, 1.0, rows)

def get_feature_json_file(config):
    model_name = config['model_name']
    if not os.path.isdir(model_name):
        os.mkdir(model_name)
    return "%s/%s" % (model_name, config['feature_json'])

def run_feature_analysis(config):
    data_info = feature_analysis.DataInfo(get_selector(config))
    features = feature_analysis.process_features(data_info)
    feature_analysis.save_features(config['feature_json'], features)
    return features


def create_row_handler(config, load_from = None):
    if isinstance(config['filter'], FeatureFilter):
        filter = config['filter']
    else:
        # For backwards compatibility let the filter be in another file loaded by name.
        module = importlib.import_module('bytegain.custom.cust.apartmentlist.%s' % config['filter'])
        filter = getattr(module, 'filter')

    features = feature_analysis.read_features(config['feature_json'])

    # Set this to experiment with weighting.
    if config['control_field']:
        print("Using '%s' as control.  Weight: %d" % (config['control_field'], config['control_weight']))
        weight_extractor = ControlWeightExtractor(config['control_field'], config['control_weight'])
        control_extractor = RowExtractor(config['control_field'])
    else:
        weight_extractor = None
        control_extractor = None

    row_handler = RowHandler(label_bucket = ValueBucket("leased", RowExtractor(config['outcome_field']), has_null = False),
                             id_extractor = RowExtractor(config['id_field']),
                             weight_extractor = weight_extractor,
                             control_extractor = control_extractor,
                             load_from = load_from,
                             extra_fields = [])
    if load_from is None:
        # print "Excluded features: %s" % str(EXCLUDED_FEATURES)
        buckets = filter.create_buckets(features)
        for bucket in buckets:
            row_handler.add_bucket(bucket)

    return row_handler

def create_row_handler_test(config, load_from = None):
    if isinstance(config['filter'], FeatureFilter):
        filter = config['filter']
    else:
        # For backwards compatibility let the filter be in another file loaded by name.
        module = importlib.import_module('bytegain.custom.cust.apartmentlist.%s' % config['filter'])
        filter = getattr(module, 'filter')

    features = feature_analysis.read_features(config['feature_json'])

    # Set this to experiment with weighting.
    if config['control_field']:
        print("Using '%s' as control.  Weight: %d" % (config['control_field'], config['control_weight']))
        weight_extractor = ControlWeightExtractor(config['control_field'], config['control_weight'])
        control_extractor = RowExtractor(config['control_field'])
    else:
        weight_extractor = None
        control_extractor = None

    row_handler = RowHandler(label_bucket = ValueBucket("leased", RowExtractor(config['outcome_field']), has_null = False),
                             id_extractor = RowExtractor(config['id_field']),
                             weight_extractor = weight_extractor,
                             control_extractor = control_extractor,
                             load_from = load_from,
                             extra_fields = [])
    if load_from is None:
        # print "Excluded features: %s" % str(EXCLUDED_FEATURES)
        buckets = filter.create_buckets(features)
        for bucket in buckets:
            row_handler.add_bucket(bucket)

    return row_handler

class ControlWeightExtractor(object):
    def __init__(self, control_field, control_weight = 1.0):
        self._control_weight = control_weight
        self._control_field = control_field
        self._field = None

    def get_fields(self):
        return [self._control_field]

    def update_fields_by_id(self, cursor_header):
        self._field = cursor_header.index(self._control_field)

    def extract(self, row):
        if self._field is not None:
            return self._control_weight if row[self._field] else 1.0
        else:
            return self._control_weight if row[self._control_field] else 1.0

    def description(self):
        return "Control weighting: %f" % self._control_weight
