import bytegain.nn_tools.auc_plot as auc_plot
import time
from threading import Thread
import abc
import numpy as np
import xgboost as xgb
import bytegain.custom.nn_tools.xgb_stats as xgb_stats


class BaseBoostClassifier(object):
    def __init__(self, loaded_classifier=None, group_function=None):
        self._group_function = group_function
        self._classifier = loaded_classifier

    @abc.abstractmethod
    def train(self, datasets, **args):
        pass

    @abc.abstractmethod
    def predict(self, dataset, **args):
        pass

    def get_sorted_results(self, dataset):
        preds = self.predict(dataset)
        results = []
        if self._group_function is None:
            for entry in zip(preds, dataset._labels, dataset._ids):
                results.append({"prob": entry[0], "pos": entry[1], "id": entry[2]})
            auc_plot.sort_results(results)
        else:
            index = 0
            for group_size in self._group_function(dataset):
                end = index + group_size
                group = []
                for i in range(index, end):
                    group.append({"prob": preds[i], "pos": dataset._labels[i], "id": dataset._ids[i]})
                index = end
                auc_plot.sort_results(group)
                results.append(group)
        return results

    @abc.abstractmethod
    def feature_scores(self, row_handler):
        pass

    @abc.abstractmethod
    def save(self, filename):
        pass


class XgbClassifier(BaseBoostClassifier):
    def _create_dmatrix(self, dataset, group_function=None):
        x = dataset._data
        y = dataset._labels
        weights = dataset._weights
        matrix = xgb.DMatrix(x, label=y, weight=weights)
        if group_function is not None:
            matrix.set_group(group_function(dataset))
        return matrix

    def train(self, datasets, max_rounds=401, max_depth=2, l2_norm=1000, min_increase_rounds = 40, gamma = 1, train_step_size = 0.40,
        subsample = 0.8, min_child_weight = 1, max_delta_step = 0, **args):
        dtrain = self._create_dmatrix(datasets.train, self._group_function)
        dtest = self._create_dmatrix(datasets.test, self._group_function)
        base_rate = np.sum(datasets.train.labels) / len(datasets.train.labels)
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
        # xgb.train returns a Booster, but let's call it 'classifier' for consistency
        self._classifier = xgb.train(self._param, dtrain, max_rounds, evallist, verbose_eval=100)

    def predict(self, dataset):
        dtest = self._create_dmatrix(dataset)
        return self._classifier.predict(dtest)

    def save(self, filename):
        self._classifier.save_model(filename)

    def dump_model(self, row_handler, filename):
        fmap = filename + ".fmap"
        self._create_feature_map(row_handler, fmap)
        self._classifier.dump_model(filename, fmap, True)

    def _create_feature_map(self, row_handler, filename):
        with open(filename, "w") as f:
            for i, bucket in enumerate(row_handler._buckets):
                f.write("%d %s q\n " % (i, bucket._name))

    def feature_scores(self, row_handler):
        return xgb_stats.compute_feature_importance(self, row_handler)


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