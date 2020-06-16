import bytegain.custom.cust.apartmentlist.al_xgb as al_xgb
import bytegain.custom.nn_tools.xgb_classifier as xgb
import bytegain.nn_tools.auc_plot as auc_plot
import bytegain.custom.cust.apartmentlist.leads_filter_170 as lf
import bytegain.custom.cust.apartmentlist.leads_from_redshift as tfl
feature_file = 'features/al_1.7.0.json'
features = tfl.run_feature_analysis(feature_file)

rh, datasets = al_xgb.create_rh_and_dataset(feature_file, random_seed=2828712, filter = lf.filter2)
classifier = xgb.XgbClassifier()
classifier.train(datasets, max_rounds=401, max_depth=4, l2_norm=400, min_child_weight=100, train_step_size=0.3, subsample=0.9)
features = classifier.feature_scores2(rh)
for feature in features:
    print("%25s: %4.1f" % (feature[0], feature[1]))

before_results = classifier.get_sorted_results(datasets.test)
before_control_results = classifier.get_sorted_results(datasets.get_test_control())

rh, datasets = al_xgb.create_rh_and_dataset(feature_file, random_seed=2828712, filter = lf.filter)
classifier = xgb.XgbClassifier()
classifier.train(datasets, max_rounds=401, max_depth=4, l2_norm=400, min_child_weight=100, train_step_size=0.3, subsample=0.9)
features = classifier.feature_scores2(rh)
for feature in features:
    print("%25s: %4.1f" % (feature[0], feature[1]))

after_results = classifier.get_sorted_results(datasets.test)
after_control_results = classifier.get_sorted_results(datasets.get_test_control())

auc_plot.plot_auc('/tmp/auc_with_prediction_all.png', before_results, results2=after_results,
                  x_label='All Notifications',
                  y_label='Percent of Leases',
                 labels= ["Existing", "With Events"])


auc_plot.plot_auc('/tmp/auc_with_prediction_control.png', before_control_results, results2=after_control_results,
                  x_label='All Notifications',
                  y_label='Percent of Leases',
                  labels= ["Existing", "With Events"])