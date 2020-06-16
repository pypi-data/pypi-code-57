import time
import numpy
import tempfile
import copy
import xgboost as xgb
import bytegain.nn_tools.auc_plot as auc_plot
import bytegain.custom.nn_tools.xgb_stats as xgb_stats
from threading import Thread

def _create_dmatrix(dataset, test = None, group_function = None):
    x = dataset._data
    y = dataset._labels
    weights = dataset._weights
    if test:
        matrix = xgb.DMatrix(x)
    else:
        matrix = xgb.DMatrix(x, label=y)
    if group_function is not None:
        matrix.set_group(group_function(dataset))
    return matrix

# Override predict to return probabilities
class MyXGBClassifier(xgb.XGBClassifier):
    def predict(self, test_dmatrix, output_margin=False, ntree_limit=0):
        # TODO(yuri): Looks like the below should be self.get_booster()
        class_probs = self.booster().predict(test_dmatrix,
                                             output_margin=output_margin,
                                             ntree_limit=ntree_limit)
        return class_probs

import numpy as np
from six import string_types
STRING_TYPES = (string_types,)

class XgbClassifier(object):
    def __init__(self, outcomes = 2, model = None, threads = 4, loaded_bst = None, group_function = None):
        """

        :param outcomes:
        :param threads:
        :param loaded_bst:
        :param group_function: If set then groups are computed and pairwise ranking is used
        """
        self._outcomes = outcomes
        self._group_function = None
        self._model = model

    def train(self, datasets, max_rounds = 401,min_increase_rounds = 40, l2_norm = 1000, gamma = 1, train_step_size = 0.40,
        subsample = 0.8, max_depth = 2, min_child_weight = 1, max_delta_step = 0 ):

        # # Let's replace the booster with the classifier. To make sure they are the same thing let's compare
        # dtrain = _create_dmatrix(datasets.train)
        # # Default XGBClassifier parameters (to compare booster and classifier)
        # self._param = {'reg_alpha': 0, 'colsample_bytree': 1, 'silent': 1, 'eval_metric': 'auc', 'colsample_bylevel': 1, 'scale_pos_weight': 1, 'learning_rate': 0.1, 'missing': None, 'max_delta_step': 0, 'base_score': 0.5, 'n_estimators': 101, 'subsample': 1, 'reg_lambda': 1, 'seed': 0, 'min_child_weight': 1, 'objective': 'binary:logistic', 'max_depth': 3, 'gamma': 0}
        # self._bst = xgb.train(self._param, dtrain, max_rounds)
        # # They give the same predictions, so let's use the classifier only

        # Let's override predict to return probabilities
        if self._model == 'booster_tuned':
            dtrain = _create_dmatrix(datasets.train, self._group_function)
            dtest = _create_dmatrix(datasets.test, self._group_function)
            base_rate = numpy.sum(datasets.train.labels) / len(datasets.train.labels)
            print('train base rate: %5.3f%%' % (base_rate * 100))
            evallist = [(dtest, 'eval'), (dtrain, 'train')]
            self._param = {'silent': True, 'objective': 'binary:logistic'}
            self._param['eval_metric'] = 'auc'
            self._param["base_score"] = base_rate
            self._param["early_stopping_rounds"] = min_increase_rounds
            self._param["gamma"] = gamma
            self._param["subsample"] = subsample
            self._param['lambda'] = l2_norm
            self._param['eta'] = train_step_size
            self._param['max_depth'] = max_depth
            self._param['min_child_weight'] = min_child_weight
            self._param['max_delta_step'] = max_delta_step
            self._bst = xgb.train(self._param, dtrain, max_rounds, evallist, verbose_eval=100)
        elif self._model == 'booster':
            self._param = {'reg_alpha': 0, 'colsample_bytree': 1, 'silent': 1, 'eval_metric': 'auc',
                           'colsample_bylevel': 1, 'scale_pos_weight': 1, 'learning_rate': 0.1, 'missing': None,
                           'max_delta_step': 0, 'base_score': 0.5, 'n_estimators': 101, 'subsample': 1, 'reg_lambda': 1,
                           'seed': 0, 'min_child_weight': 1, 'objective': 'binary:logistic', 'max_depth': 3, 'gamma': 0}
            dtrain = _create_dmatrix(datasets.train, self._group_function)
            self._bst = xgb.train(self._param, dtrain, max_rounds)
        else:
            self._classifier = MyXGBClassifier(n_estimators=max_rounds).fit(datasets.train._data, datasets.train._labels, eval_metric='auc')

    def get_sorted_results(self, dataset):
        dtest = _create_dmatrix(dataset, test=True)
        # Predict using a booster
        # preds = self._bst.predict(dtest)
        # Predict using a classifier
        # preds1 = self._classifier.predict(dataset._data) # classifier converts probabilities into column indices, so preds1 ! = preds
        if self._model == 'booster' or self._model == 'booster_tuned':
            preds = self._bst.predict(dtest)
        else:
            preds = self._classifier.predict(dtest)
        results = []
        if self._group_function is None:
            for entry in zip(preds, dataset._labels, dataset._ids):
                results.append({"prob" : entry[0], "pos" : entry[1], "id" : entry[2]})
            auc_plot.sort_results(results)
        else:
            index = 0
            for group_size in self._group_function(dataset):
                end = index + group_size
                group =[]
                for i in range(index, end):
                    group.append({"prob" : preds[i], "pos" : dataset._labels[i], "id" : dataset._ids[i]})
                index = end
                auc_plot.sort_results(group)
                results.append(group)

        return results

    def model_select_features(self, datasets, max_rounds):
        from numpy import sort
        # Fit model using each importance as a threshold
        model = self._classifier
        thresholds = sort(model.feature_importances_)
        from sklearn.feature_selection import SelectFromModel
        X_train = datasets.train._data
        y_train = datasets.train._labels
        X_test = datasets.test._data
        y_test = datasets.test._labels
        for thresh in thresholds:
            # select features using threshold
            selection = SelectFromModel(model, threshold=thresh, prefit=True)
            select_X_train = selection.transform(X_train)
            # train model
            selection_model = MyXGBClassifier(n_estimators=max_rounds)
            selection_model.fit(select_X_train, y_train)
            # eval model
            select_X_test = selection.transform(X_test)
            datasets.test._data = select_X_test
            auc = get_auc_model(selection_model, datasets.test)
            print("Thresh=%.3f, n=%d, AUC: %.5f%%" % (thresh, select_X_train.shape[1], auc))

    def dump_model(self, row_handler, filename):
        fmap = filename + ".fmap"
        create_feature_map(row_handler, fmap)
        self._bst.dump_model(filename, fmap, True)

    def feature_scores(self, row_handler):
        with tempfile.NamedTemporaryFile(delete = False, suffix=".fmap") as fmap:
            create_feature_map(row_handler, fmap.name)
            feature_dict = self._bst.get_fscore(fmap.name)
            features = [(k, v) for k,v in list(feature_dict.items())]
            features = sorted(features, key = lambda x: x[1], reverse = True)
            return features

    def feature_scores2(self, row_handler):
        return xgb_stats.compute_feature_importance(self, row_handler)

    def save(self, filename):
        self._bst.save_model(filename)


def get_auc_model(model, dataset):
    dtest = _create_dmatrix(dataset, test=True)
    preds = model.predict(dtest)
    results = []
    for entry in zip(preds, dataset._labels, dataset._ids):
        results.append({"prob" : entry[0], "pos" : entry[1], "id" : entry[2]})
    auc_plot.sort_results(results)
    auc = auc_plot.compute_auc(results)
    return auc

def create_feature_map(row_handler, filename):
    with open(filename, "w") as f:
        for i, bucket in enumerate(row_handler._buckets):
            f.write("%d %s q\n " % (i, bucket._name))

def get_params(params):
    k, v = next(iter(list(params.items())))
    new_params = copy.copy(params)
    del new_params[k]
    if type(v) not in (tuple, list):
        v = [v]
    total_runs = []
    if len(new_params) > 0:
        runs = get_params(new_params)
        for value in v:
            new_runs = copy.deepcopy(runs)
            for new_run in new_runs:
                new_run[k] = value
            total_runs.extend(new_runs)
    else:
        for value in v:
            total_runs.append({k : value})
    return total_runs

def run_hyper_param(dataset, params):
    runs = get_params(params)
    print("Total runs: %d" % len(runs))
    outcomes = []
    for run in runs:
        net = XgbClassifier()
        net.train(dataset, **run)
        results = net.get_sorted_results(dataset.test)
        auc = auc_plot.compute_auc(results)
        outcomes.append((auc, run))
        print("AUC: %6.4f %s" % (auc, str(run)))

    outcomes = sorted(outcomes, key = lambda x: x[0], reverse = True)

    for run in outcomes:
        print("AUC: %6.4f %s" % (run[0], str(run[1])))

class CvRunner(Thread):
    def __init__(self, fold, dataset, net, training_cycles, train_args):
        super(CvRunner, self).__init__()
        self._net = net
        self._fold = fold
        self._dataset = dataset
        self._training_cycles = training_cycles
        self._train_args = train_args

    def run(self):
        print("Running CV fold: %d" % self._fold)

        self._net.train(datasets=self._dataset, max_rounds = self._training_cycles, **self._train_args)
        self._sorted_test = self._net.get_sorted_results(self._dataset.test)

class ClonedDatasets(object):
    def __init__(self, datasets):
        self.train = datasets.train.copy()
        self.test = datasets.test.copy()

def cv(dataset, create_net, training_cycles = 361, runs = 5, parallel = False, **train_args):
    start_time = time.time()
    auc_sum = 0
    aucs = []
    test_results = []
    runners = []
    for run in range(runs):
        clone_dataset = ClonedDatasets(dataset) if parallel else dataset
        net = create_net(threads = 3) if parallel else create_net()
        runner = CvRunner(run, clone_dataset, net, training_cycles, train_args)
        runners.append(runner)
        if parallel:
            runner.start()
        else:
            runner.run()

        if run < runs - 1:
            dataset.repartition()

    if parallel:
        for thread in runners:
            thread.join()

    for runner in runners:
        sorted_test = runner._sorted_test
        aucs.append(auc_plot.compute_auc(sorted_test))
        test_results.extend(sorted_test)

    auc_plot.sort_results(test_results)
    auc = auc_plot.compute_auc(test_results)
    print("CV time: %5.3fs" % (time.time() - start_time))
    print("Total Auc: %5.3f %s" % (auc, str([("%5.3f" % a) for a in aucs])))
    print("Average Auc: %5.3f" % float(sum(aucs)/len(aucs)))
    return test_results
