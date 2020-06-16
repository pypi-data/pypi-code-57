import pyximport

pyximport.install()

import bytegain.custom.cust.apartmentlist.al_xgb as al_xgb
import bytegain.nn_tools.auc_plot as auc_plot
import bytegain.custom.cust.apartmentlist.leads_filter_160 as lf160
import time
import bytegain.custom.nn_tools.xgb_classifier as xgb

# Data with prediction
feature_file = 'bytegain/cust/apartmentlist/features/al_prob1.json'
# features = tfl.run_feature_analysis(feature_file)
rh, datasets = al_xgb.create_rh_and_dataset(feature_file, downsample_negative=False, random_seed=2828712, filter = lf160.filter)

n_rounds = 500

models = {'xgb': xgb.XgbClassifier()}

for model_name in list(models.keys()):
    print("Training the %s classifier"%model_name)
    time0 = time.time()
    classifier = models[model_name]
    classifier.train(datasets, max_rounds=401, max_depth=4, l2_norm=1000, subsample=0.9, train_step_size=0.3,
                     min_child_weight=100)
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
