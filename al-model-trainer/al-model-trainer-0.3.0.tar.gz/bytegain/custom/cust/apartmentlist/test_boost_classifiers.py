import pyximport

pyximport.install()

import bytegain.custom.cust.apartmentlist.al_xgb as al_xgb
import bytegain.nn_tools.auc_plot as auc_plot
import bytegain.custom.cust.apartmentlist.leads_filter_160 as lf160
import time
import bytegain.custom.nn_tools.boost_classifiers as bst_classes

# import leads_from_redshift as tfl
# feature_file = 'features/al_1.6.1.json'
# features = tfl.run_feature_analysis(feature_file)
feature_file = 'features/al_1.6.1.json'
rh, datasets = al_xgb.create_rh_and_dataset(feature_file, downsample_negative=False, random_seed=2828712, filter = lf160.filter)

n_rounds = 500

models = {'cat': bst_classes.CatClassifier(), 'xgb': bst_classes.XgbClassifier(), 'light': bst_classes.LightGBMClassifier()}

for model_name in list(models.keys()):
    print("Training the %s classifier"%model_name)
    time0 = time.time()
    classifier = models[model_name]
    classifier.train(datasets, max_rounds=n_rounds, max_depth=4, l2_norm=1000, min_child_weight=200)
    print("Took %.5f sec to train %s"%(time.time() - time0, model_name))
    features = classifier.feature_scores(rh)
    print("--------------------")
    for feature in features:
        print("%25s: %4.1f" % (feature[0], feature[1]))
    results = classifier.get_sorted_results(datasets.test)
    print("--------------------")
    print("The AUC for the %s is %.5f"%(model_name, auc_plot.compute_auc(results)))
    print("--------------------")
    auc_plot.plot_auc('/tmp/auc_'+model_name+'.png', results)
