"""
metrics.py
written in Python3
author: C. Lockhart <chris@lockhartlab.org>
"""

from ._utilities import _coerce_sample_weights, _coerce_y_prob, classify

from functools import partial
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix
from scipy.stats import ks_2samp


# Accuracy computed from confusion matrix
def _accuracy(cm):
    """
    Compute the accuracy from the confusion matrix

    Parameters
    ----------
    cm : pd.DataFrame
        Confusion matrix values

    Returns
    -------
    float
        Accuracy for each class
    """

    # Components
    fn = _false_negatives(cm)
    fp = _false_positives(cm)
    tn = _true_negatives(cm)
    tp = _true_positives(cm)

    # Then, the accuracy is the sum along the diagonal when true class = predicted class divided by all predictions
    return (tp + tn) / (tp + tn + fp + fn)


# Compute the f1 score from confusion matrix
def _f1(cm):
    """
    Compute the f1 score from the confusion matrix

    Parameters
    ----------
    cm : numpy.ndarray
        Confusion matrix values

    Returns
    -------
    numpy.ndarray
        f1 score for each class
    """

    # Components
    fn = _false_negatives(cm)
    fp = _false_positives(cm)
    tp = _true_positives(cm)

    # Return
    return 2.0 * tp / (2.0 * tp + fp + fn)


# Compute false negatives from the confusion matrix
def _false_negatives(cm):
    """
    Extract false negatives from the confusion matrix

    As an example, consider the table below.

    +--------+---+-----------+
    |        |   | Predicted |
    +--------+---+---+---+---+
    |        |   | A | B | C |
    +--------+---+---+---+---+
    | Actual | A | 1 | 2 | 3 |
    |        +---+---+---+---+
    |        | B | 4 | 5 | 6 |
    |        +---+---+---+---+
    |        | C | 7 | 8 | 9 |
    +--------+---+---+---+---+

    False negatives for class A are those where we predicted class B or C but the actual class was A. In other words,
    we can take the sum of the actual A row and subtract the true positive for A, i.e., 1 + 2 + 3 - 1 = 5. Similarly,
    for B we get 4 + 5 + 6 - 5 = 10, and for C we get 7 + 8 + 9 - 9 = 15.

    Parameters
    ----------
    cm : numpy.ndarray
        Confusion matrix values

    Returns
    -------
    numpy.ndarray
        Number of false negatives for each class
    """

    # Computed as the sum of actual positives - true positives
    return np.sum(cm, axis=1) - _true_positives(cm)


# Compute false positives from the confusion matrix
def _false_positives(cm):
    """
    Extract false positives from the confusion matrix

    As an example, consider the table below.

    +--------+---+-----------+
    |        |   | Predicted |
    +--------+---+---+---+---+
    |        |   | A | B | C |
    +--------+---+---+---+---+
    | Actual | A | 1 | 2 | 3 |
    |        +---+---+---+---+
    |        | B | 4 | 5 | 6 |
    |        +---+---+---+---+
    |        | C | 7 | 8 | 9 |
    +--------+---+---+---+---+

    False positives for class A are those where we predicted class A but the actual class was B or C. In other words,
    we can take the sum of the predicted A column and subtract the true positive for A, i.e., 1 + 4 + 7 - 1 = 11.
    Similarly, for B we get 2 + 5 + 8 - 5 = 10, and for C we get 3 + 6 + 9 - 9 = 9.

    Parameters
    ----------
    cm : numpy.ndarray
        Confusion matrix values

    Returns
    -------
    numpy.ndarray
        Number of false positives for each class
    """

    # Computed as the sum of predicted positives - true positives
    return np.sum(cm, axis=0) - _true_positives(cm)


# Helper function to compute the precision from the confusion matrix
def _precision(cm):
    """
    Compute the precision from the confusion matrix

    Parameters
    ----------
    cm : numpy.ndarray
        Confusion matrix values

    Returns
    -------
    numpy.ndarray
        Precision for each class
    """

    # Components
    fp = _false_positives(cm)
    tp = _true_positives(cm)

    # Return
    return tp / (tp + fp)


# Recall
def _recall(cm):
    """
    Compute the recall from confusion matrix

    Parameters
    ----------
    cm : numpy.ndarray
        Confusion matrix values

    Returns
    -------
    numpy.ndarray
        Recall for each class
    """

    # Components
    fn = _false_negatives(cm)
    tp = _true_positives(cm)

    # Return
    return tp / (tp + fn)


# ROC
def _roc_auc(fpr, tpr):
    """
    Compute area under receiver operating characteristic (ROC) from false positives rates and true positive rates

    Parameters
    ----------
    fpr : ArrayLike
        False positive rates
    tpr : ArrayLike
        True positive rates

    Returns
    -------
    float
        Area under ROC
    """

    return np.trapz(tpr, fpr)


# Specificity
def _specificity(cm):
    """
    Compute the specificity from the confusion matrix

    Parameters
    ----------
    cm : numpy.ndarray
        Confusion matrix values

    Returns
    -------
    numpy.ndarray
        Specificity for each class
    """

    # Components
    fp = _false_positives(cm)
    tn = _true_negatives(cm)

    # Return
    return tn / (tn + fp)


# Compute true negatives from the confusion matrix
def _true_negatives(cm):
    """
    Extract true negatives from the confusion matrix

    As an example, consider the table below.

    +--------+---+-----------+
    |        |   | Predicted |
    +--------+---+---+---+---+
    |        |   | A | B | C |
    +--------+---+---+---+---+
    | Actual | A | 1 | 2 | 3 |
    |        +---+---+---+---+
    |        | B | 4 | 5 | 6 |
    |        +---+---+---+---+
    |        | C | 7 | 8 | 9 |
    +--------+---+---+---+---+

    True negatives for class A are those where we predicted class B or C and the actual class was B or C. We can
    computing the sum of the diagonal and subtracting the true positive for A, i.e., 1 + 5 + 9 - 1 = 14. Similarly,
    for B we get 1 + 5 + 9 - 5 = 10, and for C we get 1 + 5 + 9 - 9 = 6.

    Parameters
    ----------
    cm : numpy.ndarray
        Confusion matrix values

    Returns
    -------
    numpy.ndarray
        Number of true negatives for each class
    """

    # Components
    tp = _true_positives(cm)

    # The number of true negatives is equal to true positives of other classes, i.e., sum(tp) - tp
    return np.sum(tp) - tp


# Compute true positives from the confusion matrix
def _true_positives(cm):
    """
    Extract true positives from the confusion matrix

    As an example, consider the table below.

    +--------+---+-----------+
    |        |   | Predicted |
    +--------+---+---+---+---+
    |        |   | A | B | C |
    +--------+---+---+---+---+
    | Actual | A | 1 | 2 | 3 |
    |        +---+---+---+---+
    |        | B | 4 | 5 | 6 |
    |        +---+---+---+---+
    |        | C | 7 | 8 | 9 |
    +--------+---+---+---+---+

    True positives are those were we predict A and the actual class is A. We can compute this by simply looking at
    the diagonal of the confusion matrix. For A, this is 1. For B and C, this is 5 and 9, respectively.

    Parameters
    ----------
    cm : numpy.ndarray
        Confusion matrix values

    Returns
    -------
    numpy.ndarray
        Number of true positives for each class
    """

    # numpy.diag computes the # of true matches for individual classes
    return np.diag(cm)


# Accuracy
# TODO allow this to be conmputed for multiclass too
def accuracy(y_true, y_pred, sample_weights=None):
    r"""
    Compute the accuracy of the model

    We compute this by calculating the number of true positives (TP), true negatives (TN), false positives (FP), and
    false negatives (FN).

    Then, :math:`accuracy = \frac{TP+TN}{TP+TN+FP+FN}`.

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes (already classified)
    sample_weights : ArrayLike
        Weight of observations

    Returns
    -------
    dict
        Accuracy for each class

    Notes
    -----
    Related unit tests:
    1. :meth:`izzy.tests.classification.TestMetrics.test_accuracy`
    2. :meth:`izzy.tests.classification.TestMetrics.test_accuracy_random`
    """

    return dict(
        zip(
            np.unique(y_true),
            _accuracy(confusion_matrix(y_true, y_pred, sample_weights).values),
        )
    )


# Accuracy plot
def accuracy_plot(y_true, y_pred, class_weight=None):
    """
    Plot the accuracy vs the threshold

    Parameters
    ----------
    y_true
    y_pred
    class_weight

    Returns
    -------

    """

    # thresholds = np.linspace(0, 1, 0.1)
    # accuracies = np.vectorize(accuracy(y__true, y_pred))
    pass


# AIC
def aic(log_likelihood, degrees_of_freedom):
    """
    Compute the Akaike Information Criteria (AIC)

    This function penalizes the log likelihood :math:`L` by the degrees of freedom :math:`D`. Specifically,

    .. math:: AIC = -2L + 2D

    Parameters
    ----------
    log_likelihood : int or float
        The log likelihood
    degrees_of_freedom : int or float
        The degrees of freedom

    Returns
    -------
    float
        AIC
    """

    # Compute and return
    return -2.0 * log_likelihood + 2 * degrees_of_freedom


# Banana plot
# TODO give banana plot a better name
# TODO Sorted score vs recall is the official plot
# TODO you can generalize this and apply it to precision, f1, etc.
def banana_plot():
    pass


# BIC
def bic(log_likelihood, degrees_of_freedom, num_samples):
    """
    Compute the Bayesian Information Criteria (BIC)

    This function penalizes the log likelihood :math:`L` by the degrees of freedom :math:`D` and the number of samples
    :math:`N`. Specifically, we compute,

    .. math:: BIC = -2L + Dln(N)

    Parameters
    ----------
    log_likelihood : int or float
        Log likelihood
    degrees_of_freedom : int or float
        Degrees of freedom
    num_samples : integer
        Number of observations

    Returns
    -------
    float
        BIC
    """

    # Number of samples must be greater than 0
    if num_samples <= 0:
        raise ValueError("num_samples must be > 0")

    # Compute and return
    return -2.0 * log_likelihood + np.log(num_samples) * degrees_of_freedom


# Compute confusion matrix
def confusion_matrix(y_true, y_pred, sample_weights=None):
    """
    Compute the confusion matrix

    The confusion matrix is a 2D matrix that shows actual outcomes (as rows) and predicted outcomes (as columns). The
    matrix displays the counts of observations that fall into each bucket. From this, we can compute false negatives,
    false positives, true negatives, true positives, and other metrics derived from these.

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes, must already be classified
    sample_weights : ArrayLike
        Weights associated with individual observations

    Returns
    -------
    pandas.DataFrame
        Confusion matrix with classes as row and column labels
    """

    # Get classes
    classes = np.unique(y_true)
    n_classes = len(classes)

    # All unique classes in y_pred must be in y_true
    if not np.min(np.in1d(np.unique(y_pred), classes)):
        raise AttributeError("every class in y_pred must be in classes")

    # Weights
    if sample_weights is None:
        sample_weights = np.ones(len(y_true))

    # Create confusion matrix using coo_matrix (this elegant solution is from sklearn)
    cm_values = coo_matrix(
        (sample_weights, (y_true, y_pred)), shape=(n_classes, n_classes), dtype="int"
    ).toarray()

    # Turn into DataFrame
    cm = pd.DataFrame(cm_values, index=classes, columns=classes)

    # Ensure that the order of index and columns matches
    if not all(cm.index.values == cm.columns):
        raise ValueError("confusion matrix order of index and columns must match")

    # Return
    return cm


# f1 score
def f1(y_true, y_pred, sample_weights=None):
    r"""
    Compute the f1 score

    .. math:: f1 = \frac{2TP}{2TP + FP + FN}

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes, already classified
    sample_weights : ArrayLike
        Weight of observations

    Returns
    -------
    dict
        f1 score for each class

    """

    return dict(
        zip(
            np.unique(y_true),
            _f1(confusion_matrix(y_true, y_pred, sample_weights).values),
        )
    )


# Compute false negatives
def false_negatives(y_true, y_pred, sample_weights=None):
    """
    Compute false negatives

    In simpler terms, false negatives are those we say are not the target class but actually are the target class.

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    sample_weights : ArrayLike
        Weight for observations

    Returns
    -------
    dict
        False negatives for each class
    """

    return dict(
        zip(
            np.unique(y_true),
            _false_negatives(confusion_matrix(y_true, y_pred, sample_weights).values),
        )
    )


# Compute false positives
def false_positives(y_true, y_pred, sample_weights=None):
    """
    Compute false positives

    In simpler terms, false positives are those we say are the target outcome but are actually in a different class.

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    sample_weights : ArrayLike
        Weight for observations

    Returns
    -------
    dict
        False positives for each class
    """

    return dict(
        zip(
            np.unique(y_true),
            _false_positives(confusion_matrix(y_true, y_pred, sample_weights).values),
        )
    )


# Compute Gini coefficient
def gini(y_true, y_prob, sample_weights=None):
    """
    Compute the Gini coefficient

    Although there is rich literature on Gini, in practice this is simply a function of the area under the ROC
    curve (AUROC).

    .. math:: Gini = 2 * AUROC - 1

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_prob : ArrayLike
        Probabilistic outcomes
    sample_weights : ArrayLike
        Weight of observations

    Returns
    -------
    float
        Gini coefficient
    """

    # Return GINI
    return 2.0 * roc_auc(y_true, y_prob) - 1.0


# KS statistic
# TODO add weights : https://stackoverflow.com/questions/40044375/how-to-calculate-the-kolmogorov-smirnov-statistic-between-two-weighted-samplesp
def ks(y_true, y_prob, sample_weights=None):
    """
    Compute the Kolmogorov-Smirnov (KS) test statistic to evaluate model performance

    Parameters
    ----------
    y_true : ArrayLike
        True y values
    y_prob : ArrayLike
        Predicted y values (expressed as a probability when target outcome is true)
    sample_weights

    Returns
    -------
    float
        KS statistic

    See Also
    --------
    https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test
    """

    # Get classes
    classes = np.unique(y_true)
    n_classes = len(classes)

    # We can only compute this for binomial classifiers
    if n_classes != 2:
        raise AttributeError("KS requires a binomial classification problem")

    # Coerce y_prob into the correct form, but only get probabilities for target outcome
    y_prob = _coerce_y_prob(y_prob, assert_binomial=True)[:, 1]

    # Compute KS statistic
    statistic, p_value = ks_2samp(
        y_prob[y_true == classes[0]],
        y_prob[y_true == classes[1]],
        alternative="two-sided",
    )

    # Return KS statistic
    return statistic


# Compute the log-likelihood from y_true and y_prob
def log_likelihood(y_true, y_prob, normalize=True):
    """
    Compute the log likelihood from true and predicted outcomes

    Mathematically, for a sample :math:`i`, we compute the likelihood :math:`L_i = p_i^{y_i} (1-p_i)^{1-y_i}.` Here,
    we compute :math:`p` as the predicted probability and :math:`y` as the true outcome.

    We can choose to `normalize` by the number of samples to get the average log likelihood per sample.

    The procedure is to use `x` to get the predicted probabilities, and then compute :math:`L_i` above.

    Note that the log likelihood depends on the specific variables in the model, i.e., cross-comparison of models is
    with different features is technically incorrect.


    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_prob : ArrayLike
        Probabilistic outcomes
    normalize : bool
        Should we compute the average log likelihood per sample? (Default: True)

    Returns
    -------
    float
        log-likelihood
    """

    # Sanity checking
    n_classes = len(np.unique(y_true))
    if n_classes != y_prob.shape[1]:
        raise AttributeError("n_classes must match shape of y_prob")

    # Transform y_true into an expanded form
    y_true = np.eye(n_classes)[np.array([y_true], dtype="int").reshape(-1)]

    # Return log likelihood
    f = np.mean if normalize else np.sum
    return f(np.log(np.sum(y_true * y_prob, axis=1)))


# Generate model performance report
# Note: this is a function (not GenericModel method) for external use
# TODO maybe sent x as argument, so log likelihood and degrees of freedom can be computed in function?
def performance_report(
    y_true, y_prob, degrees_of_freedom=None, threshold=0.5, sample_weights=None
):
    """
    A performance report for a model.

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_prob : ArrayLike
        Probabilistic outcomes
    degrees_of_freedom : float
        (Optional) The number degrees of freedom
    threshold : float
        The cutoff to indicate successful outcomes or not (Default: 0.5)
    sample_weights : ArrayLike
        Weight of observations

    Returns
    -------
    pandas.Series
        performance report
    """

    # Empty report container
    report = pd.Series()

    # Create y_pred
    y_pred = classify(y_prob, threshold=threshold)

    # Accuracy, precision, recall, f1
    cm = confusion_matrix(y_true, y_pred, sample_weights=sample_weights).values
    report["accuracy"] = _accuracy(cm)
    report["precision"] = _precision(cm)
    report["recall"] = _recall(cm)
    report["f1"] = _f1(cm)

    # Log-likelihood?
    if log_likelihood is not None and degrees_of_freedom is not None:
        log_likelihood_ = log_likelihood(y_true, y_prob)
        report["log-likelihood"] = log_likelihood_
        report["AIC"] = aic(log_likelihood_, degrees_of_freedom)
        report["BIC"] = bic(log_likelihood_, degrees_of_freedom, len(y_true))

    # KS statistic (only if n_classes = 2)
    if len(np.unique(y_true)) == 2:
        report["KS"] = ks(y_true, y_pred)

    # AUROC / GINI
    report["AUROC"] = roc_auc(y_true, y_pred, sample_weights=sample_weights)
    report["GINI"] = gini(y_true, y_pred, sample_weights=sample_weights)

    # TODO slope

    # TODO correlation

    # Return report
    return report


# Compute the precision
def precision(y_true, y_pred, sample_weights=None):
    """
    Compute the precision (synonym: positive predictive value)

    .. math:: precision = /frac{TP}{TP + FP}

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    sample_weights : ArrayLike
        Weight of observations

    Returns
    -------
    dict
        Precision for each class
    """

    return dict(
        zip(
            np.unique(y_true),
            _precision(confusion_matrix(y_true, y_pred, sample_weights).values),
        )
    )


# Precision synonyms
positive_predictive_value = precision


# Compute the recall
def recall(y_true, y_pred, sample_weights=None):
    """
    Compute the recall (synonyms: sensitivity, hit rate, true positive rate)

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    sample_weights : ArrayLike
        Weight for observations

    Returns
    -------
    dict
        Recall for each class
    """

    return dict(
        zip(
            np.unique(y_true),
            _recall(confusion_matrix(y_true, y_pred, sample_weights).values),
        )
    )


# Recall synonyms
sensitivity = recall
hit_rate = recall
true_positive_rate = recall


# Compute the receiver operating characteristic
def roc(y_true, y_prob, sample_weights=None):
    """
    Compute false positive rates and true positives rates for the receiver operating characteristic

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_prob : ArrayLike
        Predicted outcomes expressed as probabilities
    sample_weights : ArrayLike
        Weight of observations

    Returns
    -------
    tuple of numpy.ndarray
        False positive rates and true positive rates
    """

    # Coerce y_prob into correct form
    y_prob = _coerce_y_prob(y_prob, assert_binomial=True)[:, 1]

    # Coerce sample weights into suitable form
    sample_weights = _coerce_sample_weights(sample_weights, n_samples=len(y_true))

    # Put y_true and y_prob into DataFrame for easy use
    df = pd.DataFrame(
        {"y_true": y_true * sample_weights, "y_prob": y_prob}
    ).sort_values("y_prob", ascending=False)
    df["y_false"] = 1.0 - df["y_true"]

    # Compute TPR and FPR
    df["fpr"] = df["y_false"].cumsum() / df["y_false"].sum()
    df["tpr"] = df["y_true"].cumsum() / df["y_true"].sum()

    # Return
    return df["fpr"].values, df["tpr"].values


# Area under ROC curve
# TODO make sure that sample_weights doesn't include class weights
def roc_auc(y_true, y_prob, sample_weights=None):
    """
    Compute the area under the receiver operating characteristic (ROC) curve

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_prob : ArrayLike
        Predicted outcomes expressed as probabilities
    sample_weights : ArrayLike
        Weight of observations

    Returns
    -------
    float
        Area under the ROC curve
    """

    return _roc_auc(*roc(y_true, y_prob, sample_weights=sample_weights))


# Plot the ROC curve
def roc_plot(y_true, y_prob, sample_weights=None):
    """
    Plot the receiver operating characteristic (ROC)

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_prob : ArrayLike
        Probabilistic outcomes
    sample_weights : ArrayLike
        Weight of observations
    """

    # Calculate FPR, TPR
    fpr, tpr = roc(y_true, y_prob, sample_weights=sample_weights)

    # Compute the area under the curve
    auroc = np.round(_roc_auc(fpr, tpr), 2)

    # Plot
    # TODO change this to izviz plot, make customizable with kwargs
    plt.figure(figsize=(20, 10))
    plt.plot(fpr, tpr, label="AUROC = {}".format(auroc))
    plt.xlabel("False positive rate")
    plt.ylabel("True positive rate")
    plt.title("Receiver operating characteristic")
    plt.legend()
    plt.show()


# Compute the specificity
def specificity(y_true, y_pred, sample_weights=None):
    """
    Compute the specificity (synonyms: selectivity, true negative rate)

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    sample_weights : ArrayLike
        Weight for individual observations

    Returns
    -------
    dict
        Specificity for each class
    """

    # Return as dictionary
    return dict(
        zip(
            np.unique(y_true),
            _specificity(confusion_matrix(y_true, y_pred, sample_weights).values),
        )
    )


# Specificity synonyms
selectivity = specificity
true_negative_rate = specificity


# Compute true negatives
def true_negatives(y_true, y_pred, sample_weights=None):
    """
    Compute true negatives

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    sample_weights : ArrayLike
        Weight for observations

    Returns
    -------
    dict
        True negatives for each class
    """

    return dict(
        zip(
            np.unique(y_true),
            _true_negatives(confusion_matrix(y_true, y_pred, sample_weights).values),
        )
    )


# Compute true positives
def true_positives(y_true, y_pred, sample_weights=None):
    """
    Compute true positives

    Parameters
    ----------
    y_true : ArrayLike
        True outcomes
    y_pred : ArrayLike
        Predicted outcomes
    sample_weights : ArrayLike
        Weight for observations

    Returns
    -------
    dict
        True positives for each class
    """

    return dict(
        zip(
            np.unique(y_true),
            _true_positives(confusion_matrix(y_true, y_pred, sample_weights).values),
        )
    )


# Compute Weight of Evidence
# TODO fill out
# TODO move to features
def weight_of_evidence(x, y, bins=10, mode="equal"):
    pass
