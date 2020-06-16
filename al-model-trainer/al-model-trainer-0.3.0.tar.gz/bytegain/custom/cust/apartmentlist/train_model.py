import argparse
import importlib
import bytegain.custom.nn_tools.xgb_classifier as xgb
from bytegain.custom.cust.apartmentlist import al_xgb
from bytegain.custom.nn_tools import model_utils
import dill
import os
import sys
import numpy
import csv
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
import optuna
import logging
import pandas


params_dict = {'gamma':[50,100],
          'max_depth': [2,3],
          'min_child_weight':[500,1000,2000],
          'l2_norm': [50,100,200],
          'l1_norm': [50,100,200],
          'scale_pos_weight':[20,50,100]}


threshold_auc = 0.1
parser = argparse.ArgumentParser(description='Trains an AL model',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--model_config', required=True, help='filename of model_config')
parser.add_argument('--feature_analysis', action='store_true', help='If set then a new feature analysis is done')
parser.add_argument('--production', action='store_true', help='If set then push model to production')
parser.add_argument('--test_swap', action='store_true', help='test on other data')
parser.add_argument('--use_saved_model', action='store_true', help='use pre-trained model')
parser.add_argument('--grid_search', action='store_true', help='find optimal hyperparameters')
parser.add_argument('--optuna', action='store_true', help='Bayesian hyperparameter tuning')
parser.add_argument('--optuna_time', action='store_true', help='Bayesian hyperparameter tuning with a time-ordered train/eval split')
parser.add_argument('--time_order', action='store_true', help='training with a time-ordered train/eval split')
parser.add_argument('--test_frac', type=float, default =0.2, help='testing fraction, default is 0.2')
parser.add_argument('--production_time', action='store_true', help='If set then push model to production with time-ordered training')
args = parser.parse_args()

model_config = args.model_config

module = importlib.import_module('bytegain.custom.cust.apartmentlist.%s' % model_config)
config = getattr(module, 'prod_config' if args.production else 'config')

config_test = getattr(module, 'test_config' if args.test_swap else 'config')

if args.feature_analysis and not args.test_swap:
	al_xgb.run_feature_analysis(config)

if args.test_swap:
	if args.feature_analysis:
		#al_xgb.run_feature_analysis(config)
		print("Avoid running feature analysis when training and testing sets are partitioned. Feature labels may not exist in both!")

	if args.use_saved_model:
		rh, dataset = al_xgb.create_rh_and_dataset(config_test,testing_fraction = 0.99)
		test = al_xgb.test_from_dataset(config_test, rh, dataset)
	else:
		rh, dataset = al_xgb.create_rh_and_dataset(config, testing_fraction = 0.01)
		rh_test, test_set = al_xgb.create_rh_and_dataset(config_test, testing_fraction = 0.99)
		model = xgb.XgbClassifier()
		model.train(dataset, min_child_weight=config['min_child_weight'], max_rounds=config['max_rounds'],
			max_depth=config['max_depth'], l2_norm = config['l2_norm'], train_step_size = config['train_step_size'])
		control_results = model.get_sorted_results(test_set)
		print("Control AUC: %5.3f" % auc_plot.compute_auc(control_results))
		print("Control AVG PR: %5.3f" % auc_plot.compute_avgpr(control_results))
		print("Control F_BETA: %5.3f" % auc_plot.f_beta_DLMavg(control_results, beta = 10.))
		auc_plot.plot_auc('./auc_curve.png', control_results)
		#print(auc_plot.compute_metrics(control_results,threshold_auc))
		metrics_list2 = []
		metrics_list2 = auc_plot.compute_TPFN_Thresholds(control_results, minority_class_proportion = 0.0027, sample_size = 300000)
		with open("full_metrics_test_fast.csv", "w", newline="") as g:
			writer = csv.writer(g)
			writer.writerows(metrics_list2)
		auc_plot.save_predictions(control_results, filename="test_only_true_and_pred.csv")
		print("Control Revenue Voltage: $ %5.3f" % auc_plot.compute_revenue_voltage(control_results, minority_class_proportion = config_test['minority_class_prop'], sample_size = 300000))

		print('finito')



elif args.optuna:
	rh, dataset = al_xgb.create_rh_and_dataset(config, testing_fraction = 0.2)
	output_set = xgb.run_optuna(dataset)

elif args.optuna_time:
	rh, dataset = al_xgb.create_rh_and_dataset(config, testing_fraction = 0.2, shufflerows=False)
	output_set = xgb.run_optuna(dataset)

elif args.time_order:
	test_frac = 0.2
	if args.test_frac:
		test_frac = args.test_frac
	rh, dataset = al_xgb.create_rh_and_dataset(config, testing_fraction = test_frac, shufflerows=False)
	trained_model = al_xgb.train_from_dataset(config, rh, dataset)

elif args.grid_search:
	rh, dataset = al_xgb.create_rh_and_dataset(config, testing_fraction = 0.2)
	output_set = xgb.run_hyper_param_rv(dataset, params_dict)
	print(output_set)
	with open("grid_search.csv","w", newline="") as out:
		csv_out=csv.writer(out)
		csv_out.writerow(['voltage','AUCROC','parameters'])
		for row in output_set:
			csv_out.writerow(row)
		
else:
	rh, dataset = al_xgb.create_rh_and_dataset(config, testing_fraction = 0.2)
	trained_model = al_xgb.train_from_dataset(config, rh, dataset)
	import dill
	with open("./new_xgb_model_dump.pkl", "wb") as dill_file:
		dill.dump(trained_model, dill_file)


if args.production:
    al_xgb.train_and_push(config)

if args.production_time:
	test_frac = 0.2
	if args.test_frac:
		test_frac = args.test_frac
	al_xgb.train_and_push_time(config, tf = test_frac)