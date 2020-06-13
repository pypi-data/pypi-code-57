"""
test_metrics.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from izzy.classification import LogisticRegression
from izzy.classification.metrics import *

from hypothesis import given, settings
import hypothesis.strategies as st
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from sklearn.datasets import load_breast_cancer
import sklearn.metrics as sk_m
import unittest

# Hypothesis settings
settings.register_profile('lenient', deadline=None)
settings.load_profile('lenient')


# Test metrics
class TestMetrics(unittest.TestCase):
    # Bulk test for metrics derived from the confusion matrix
    @settings(deadline=None)
    @given(st.floats(min_value=0.2, max_value=0.8))
    def test_confusion_matrix(self, threshold):
        # Compute y_prob, y_pred
        y_true, y_prob, y_pred = _get_model_data(threshold)

        # Compute confusion matrix
        fn1, fp1, tn1, tp1 = _get_fn_fp_tn_tp(y_true, y_pred, 2)
        cm = confusion_matrix(y_true, y_pred).values
        fn2, fp2, tn2, tp2 = cm[1, 0], cm[0, 1], cm[0, 0], cm[1, 1]

        # Accuracy
        np.testing.assert_equal((tp1 + tn1) / (tp1 + tn1 + fp1 + fn1), list(accuracy(y_true, y_pred).values()))

        # Confusion matrix
        np.testing.assert_equal(fn1[1], fn2)
        np.testing.assert_equal(fp1[1], fp2)
        np.testing.assert_equal(tp1[1], tp2)
        np.testing.assert_equal(tn1[1], tn2)

        # f1 score
        np.testing.assert_equal(2. * tp1 / (2. * tp1 + fp1 + fn1), list(f1(y_true, y_pred).values()))

        # False negatives
        np.testing.assert_equal(fn1, list(false_negatives(y_true, y_pred).values()))

        # False positives
        np.testing.assert_equal(fp1, list(false_positives(y_true, y_pred).values()))

        # Log-likelihood
        self.assertIsInstance(log_likelihood(y_true, y_prob), float)
        self.assertIsInstance(log_likelihood(y_true, y_prob, normalize=True), float)

        # Precision
        np.testing.assert_equal(tp1 / (tp1 + fp1), list(precision(y_true, y_pred).values()))
        np.testing.assert_equal(tp1 / (tp1 + fp1), list(positive_predictive_value(y_true, y_pred).values()))

        # Recall
        np.testing.assert_equal(tp1 / (tp1 + fn1), list(recall(y_true, y_pred).values()))
        np.testing.assert_equal(tp1 / (tp1 + fn1), list(sensitivity(y_true, y_pred).values()))
        np.testing.assert_equal(tp1 / (tp1 + fn1), list(hit_rate(y_true, y_pred).values()))
        np.testing.assert_equal(tp1 / (tp1 + fn1), list(true_positive_rate(y_true, y_pred).values()))

        # Specificity
        np.testing.assert_equal(tn1 / (tn1 + fp1), list(specificity(y_true, y_pred).values()))
        np.testing.assert_equal(tn1 / (tn1 + fp1), list(selectivity(y_true, y_pred).values()))
        np.testing.assert_equal(tn1 / (tn1 + fp1), list(true_negative_rate(y_true, y_pred).values()))

        # True negatives
        np.testing.assert_equal(tn1, list(true_negatives(y_true, y_pred).values()))

        # True positives
        np.testing.assert_equal(tp1, list(true_positives(y_true, y_pred).values()))

    # Test confusion matrix metrics using random data
    @settings(deadline=None)
    @given(st.integers(min_value=2, max_value=10), st.integers(min_value=100, max_value=100000))
    def test_confusion_matrix_random(self, n_classes, n_samples):
        # Generate data
        y_true, y_pred = _get_random_data(n_classes, n_samples)

        # Compute confusion matrix
        fn1, fp1, tn1, tp1 = _get_fn_fp_tn_tp(y_true, y_pred, n_classes)

        # Accuracy
        a = (tp1 + tn1) / (tp1 + tn1 + fp1 + fn1)
        b = list(accuracy(y_true, y_pred).values())
        np.testing.assert_equal(a, b)

        # False negatives
        a = fn1
        b = list(false_negatives(y_true, y_pred).values())
        np.testing.assert_equal(a, b)

        # False positives
        a = fp1
        b = list(false_positives(y_true, y_pred).values())
        np.testing.assert_equal(a, b)

        # True negatives
        a = tn1
        b = list(true_negatives(y_true, y_pred).values())
        np.testing.assert_equal(a, b)

        # True positives
        a = tp1
        b = list(true_positives(y_true, y_pred).values())
        np.testing.assert_equal(a, b)

    # Test that we know how to compute AIC
    @settings(deadline=None)
    @given(st.floats(allow_nan=False), st.integers())
    def test_aic(self, log_likelihood, degrees_of_freedom):
        # We can compute this here and from the function
        value1 = -2 * log_likelihood + 2 * degrees_of_freedom
        value2 = aic(log_likelihood, degrees_of_freedom)

        # These must be equal
        self.assertEqual(value1, value2)

    # Test that we know how to compute BIC
    @settings(deadline=None)
    @given(st.floats(allow_nan=False), st.integers(), st.integers(min_value=1, max_value=1000000))
    def test_bic(self, log_likelihood, degrees_of_freedom, num_samples):
        # We can compute this here and from the function
        value1 = -2 * log_likelihood + np.log(num_samples) * degrees_of_freedom
        value2 = bic(log_likelihood, degrees_of_freedom, num_samples)

        # These must be equal
        self.assertEqual(value1, value2)

    # Test GINI
    def test_gini(self):
        # Generate data
        y_true, y_prob, _ = _get_model_data()
        y_prob = y_prob[:, 1]

        # We can also test the AUC as a separate test
        gini0 = sk_m.roc_auc_score(y_true, y_prob) * 2. - 1.
        gini1 = gini(y_true, y_prob)

        # Assert equal
        np.testing.assert_almost_equal(gini0, gini1, decimal=2)

    # Test KS
    def test_ks(self):
        # Generate data
        y_true, y_prob, _ = _get_model_data()
        y_prob = y_prob[:, 1]

        # We can also test the AUC as a separate test
        ks0, _ = ks_2samp(y_prob[y_true == 0], y_prob[y_true == 1], alternative='two-sided')
        ks1 = ks(y_true, y_prob)

        # Assert equal
        np.testing.assert_almost_equal(ks0, ks1, decimal=2)

    # Test that we can compute ROC using a simple model
    def test_roc(self):
        # Generate data
        y_true, y_prob, _ = _get_model_data()

        # Test
        _test_roc(y_true, y_prob[:, 1])

    # Test that we can compute ROC using random data
    @settings(deadline=None)
    @given(st.integers(min_value=100, max_value=100000))
    def test_roc_random(self, n_samples):
        # Generate data
        y_true = np.random.randint(low=0, high=2, size=n_samples)
        y_prob = np.random.rand(n_samples)

        # Test
        _test_roc(y_true, y_prob)

    # Test that we can compute AUROC using a simple model
    def test_roc_auc(self):
        # Generate data
        y_true, y_prob, _ = _get_model_data()

        # Test
        _test_roc_auc(y_true, y_prob[:, 1])

    # Test that we can compute AUROC using random data
    @settings(deadline=None)
    @given(st.integers(min_value=100, max_value=100000))
    def test_roc_auc_random(self, n_samples):
        # Generate data
        y_true = np.random.randint(low=0, high=2, size=n_samples)
        y_prob = np.random.rand(n_samples)

        # Test
        _test_roc_auc(y_true, y_prob)


# Helper function to get model data
def _get_model_data(threshold=0.5):
    # Import breast_cancer dataset
    data = load_breast_cancer()
    df = pd.DataFrame(data.data, columns=data.feature_names)
    df['target'] = data['target']

    # Train a simple predictive model
    x = df[['mean radius']]
    y = df['target']
    model = LogisticRegression(penalty='none', solver='lbfgs', class_weight='balanced')
    model.fit(x, y)

    # We will return y and y_prob
    y_prob = model.evaluate(x)
    y_pred = model.classify(x, threshold=threshold)

    # Return
    return y, y_prob, y_pred


# Helper function to compute FN, FP, TN, TP
def _get_fn_fp_tn_tp(y_true, y_pred, n_classes):
    # Zero out arrays to store results
    fp = np.zeros(n_classes)
    fn = np.zeros(n_classes)
    tp = np.zeros(n_classes)
    tn = np.zeros(n_classes)

    # Loop over all classes and compute
    for k in range(n_classes):
        # For 3 classes, if we're predicting the first class we would see
        # TP FN FN    TN FP TN    TN TN FP
        # FP TN TN    FN TP FN    TN TN FP
        # FP TN TN    TN FP TN    FN FN TP
        # The bottom squares are all TN because in a one-vs-rest scheme, these are true negatives
        # TODO implement accuracy in a true multiclass scheme
        fn[k] = np.sum((y_true == k) & (y_pred != k))
        fp[k] = np.sum((y_true != k) & (y_pred == k))
        tp[k] = np.sum((y_true == y_pred) & (y_true == k))
        tn[k] = np.sum((y_true == y_pred) & (y_true != k))

    # Return
    return fn, fp, tn, tp


# Helper function to get random data for tests
def _get_random_data(n_classes, n_samples):
    # Generate y_true; must contain every class
    while True:
        y_true = np.random.randint(low=0, high=n_classes, size=n_samples)
        if np.min(np.in1d(np.arange(n_classes), y_true)):
            break

    # Generate y_pred
    y_pred = np.random.randint(low=0, high=n_classes, size=n_samples)

    # Return
    return y_true, y_pred


# Helper function to test ROC computation
def _test_roc(y_true, y_prob):
    # Get false positive rates, true positive rates
    fpr0, tpr0, _ = sk_m.roc_curve(y_true, y_prob)
    fpr1, tpr1 = roc(y_true, y_prob)

    # Put together into DataFrames and merge
    df0 = pd.DataFrame({'fpr0': fpr0, 'tpr0': tpr0}).pivot_table(index='fpr0', values='tpr0', aggfunc='max')
    df1 = pd.DataFrame({'fpr1': fpr1, 'tpr1': tpr1}).pivot_table(index='fpr1', values='tpr1', aggfunc='max')
    df = df0.merge(df1, how='inner', left_index=True, right_index=True)

    # Assert equal
    np.testing.assert_almost_equal(df['tpr0'].values, df['tpr1'].values, decimal=2)


# Helper function to test AUROC computation
def _test_roc_auc(y_true, y_prob):
    # We can also test the AUC as a separate test
    auc0 = sk_m.roc_auc_score(y_true, y_prob)
    auc1 = roc_auc(y_true, y_prob)

    # Assert equal
    np.testing.assert_almost_equal(auc0, auc1, decimal=2)

