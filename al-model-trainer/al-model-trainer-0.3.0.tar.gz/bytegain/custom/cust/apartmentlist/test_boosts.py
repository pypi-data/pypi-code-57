import pyximport

pyximport.install()

import bytegain.custom.cust.apartmentlist.al_xgb as al_xgb
import bytegain.nn_tools.auc_plot as auc_plot
import bytegain.custom.cust.apartmentlist.leads_filter_160 as lf160
import time

import bytegain.custom.nn_tools.xg_classifier_test as test_gxb

# import leads_from_redshift as tfl
# feature_file = 'features/al_1.6.1.json'
# features = tfl.run_feature_analysis(feature_file)

feature_file = 'features/al_1.6.1.json'
rh, datasets = al_xgb.create_rh_and_dataset(feature_file, downsample_negative=False, random_seed=2828712, filter = lf160.filter)

n_rounds = 500
# XGBoost classifier
print("Training the default XGBoost classifier")
time0 = time.time()
classifier = test_gxb.XgbClassifier()
classifier.train(datasets, max_rounds=n_rounds, max_depth=4, l2_norm=1000, min_child_weight=200)
print("Feature importances")
feature_importances = classifier._classifier.feature_importances_.tolist()
imp_list = []
for i in range(len(feature_importances)):
    imp_list.append((rh._buckets[i]._name, feature_importances[i]))
    # print "Index %d, %s: %s"%(i, rh._buckets[i]._name, feature_importances[i])
imp_list.sort(key=lambda x: x[1], reverse=True)
for i in range(len(imp_list)):
    print("%25s: %4.1f"%(imp_list[i][0], imp_list[i][1]*100))
results = classifier.get_sorted_results(datasets.test)
# results = test_gxb.cv(datasets, xgb.XgbClassifier, 500, parallel=True, max_depth=4, l2_norm=1000, train_step_size=0.3, subsample=0.9, min_child_weight=50)
print("--------------------")
print("The AUC for the default XGBoost classifier is %.5f"%auc_plot.compute_auc(results))
print("--------------------")
auc_plot.plot_auc('auc_xgb.png', results)
# Feature selection
# classifier.model_select_features(datasets, 500)

# ===================================================
# Default XGBooster
print("Training the defaut XGBooster")
time0 = time.time()
classifier = test_gxb.XgbClassifier(model='booster')
classifier.train(datasets, max_rounds=500, max_depth=4, l2_norm=1000, min_child_weight=200)
print("Took %.5f sec to train the defaut XGBooster"%(time.time() - time0))
features = classifier.feature_scores2(rh)
print("--------------------")
for feature in features:
    print("%25s: %4.1f" % (feature[0], feature[1]))
results = classifier.get_sorted_results(datasets.test)
print("The AUC for the default booster is %.5f"%auc_plot.compute_auc(results))
auc_plot.plot_auc('auc_xgb.png', results)

# ===================================================
# Tuned XGBooster
print("Training the tuned XGBooster")
time0 = time.time()
classifier = test_gxb.XgbClassifier(model='booster_tuned')
classifier.train(datasets, max_rounds=n_rounds, max_depth=4, l2_norm=1000, min_child_weight=200)
print("Took %.5f sec to train the tuned XGBooster"%(time.time() - time0))
features = classifier.feature_scores2(rh)
print("--------------------")
for feature in features:
    print("%25s: %4.1f" % (feature[0], feature[1]))
results = classifier.get_sorted_results(datasets.test)
# results = test_gxb.cv(datasets, xgb.XgbClassifier, 401, parallel=True, max_depth=4, l2_norm=1000, train_step_size=0.3, subsample=0.9, min_child_weight=50)
print("--------------------")
print("The AUC for the tuned booster is %.5f"%auc_plot.compute_auc(results))
print("--------------------")
auc_plot.plot_auc('auc_xgb_tuned.png', results)
