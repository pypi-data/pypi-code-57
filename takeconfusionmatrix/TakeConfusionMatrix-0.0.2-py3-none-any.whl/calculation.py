import pandas as pd
import numpy as np

from sklearn.preprocessing import normalize as norm
from sklearn.utils import check_consistent_length, check_scalar

from .validation import check_value_mapped, check_array_size


class MetricsCalculator():
    """Calculates confusion matrix and ML metrics using batch results.

    This class is resposible for computing and calculating the confusion
    matix of the results, which afterwards will be used to assist the 
    metrics calculation.

    Parameters
    ----------
    labels: 1d array-like, or label indicator array.
        List of labels that will be computed.
    """

    def __init__(self, labels):
        check_scalar(labels, 'labels', (list, np.ndarray))
        check_array_size(labels, 'labels', 1)

        self.__labels = np.array(labels)
        self.__labels_map = {label: True for label in self.__labels}

        self.__init_confusion_matrix()

    def __init_confusion_matrix(self):
        n = self.__labels.size
        self.__confusion_matrix = pd.DataFrame(np.zeros((n, n)),
                                               index=self.__labels,
                                               columns=self.__labels)

    def compute_matrix(self, y_true, y_pred):
        """Compute confusion matrix.

        According to `scikit-learn`, a confusion matrix :math:`C_{i,j}`
        is equal to the number of observations known to be in group 
        :math: `i` and predicted to be in group :math:`j`.

        Read more in the `scikit-learn` confusion matrix documentation.

        Parameters
        ----------
        y_true : 1d array-like, or label indicator array
            Ground truth (correct) target values.

        y_pred : 1d array-like, or label indicator array
            Estimated target as returned by a classifier.

        References
        ----------
        .. [1] `scikit-learn confusion matrix documentation
                <https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html>`

        Examples
        --------
        ```python
        >>> from take_confusion_matrix import MetricsCalculation
        >>> labels = [0, 1, 2]
        >>> mc = MetricsCalculator(labels)
        >>> y_true = [0, 1, 0, 1]
        >>> y_pred = [0, 0, 0, 0]
        >>> mc.compute_matrix(y_true, y_pred)
        >>> y_true = [0, 2, 0, 2]
        >>> y_pred = [0, 0, 0, 0]
        >>> mc.compute_matrix(y_true, y_pred)
        ```
        """

        check_scalar(y_true, 'y_true', (list, np.ndarray))
        check_scalar(y_pred, 'y_pred', (list, np.ndarray))
        check_consistent_length(y_true, y_pred)
        check_value_mapped(self.__labels_map, y_true)
        check_value_mapped(self.__labels_map, y_pred)

        for i in range(len(y_true)):
            self.__confusion_matrix[y_true[i]][y_pred[i]] += 1.

    def generate_confusion_matrix(self, normalize=False,
                                  with_labels=True, labels=None) -> pd.DataFrame:
        """Generate and output confusion matrix.

        Parameters
        ----------
        normalize : bool, default = False
            If True, return output normalized using L1 normalization.

        with_labels : bool, default = True
            If False, return output without previous initialized labels.

        labels : 1d array-like, shape = n_classes, default = None
            List of labels to index the matrix.

        Returns
        -------
        C : pandas.DataFrame / ndarray, shape = (n_classes, n_classes)
            Confusion matrix whose i-th row and j-th column entry
            indicates the number of samples with true label being
            j-th class and predicted label beign i-th class.

        Examples
        --------
        ```python
        >>> from take_confusion_matrix import MetricsCalculation
        >>> labels = [0, 1, 2]
        >>> mc = MetricsCalculator(labels)
        >>> y_true = [2, 0, 2, 2, 0, 1]
        >>> y_pred = [0, 0, 2, 2, 0, 2]
        >>> mc.compute_matrix(y_true, y_pred)
        >>> mc.generate_confusion_matrix()
             0    1    2
        0  2.0  0.0  1.0
        1  0.0  0.0  0.0
        2  0.0  1.0  2.0
        >>> labels = ["class_0", "class_1","class_2"]
        >>> mc.generate_confusion_matrix(labels=labels)
                class_0  class_1  class_2
        class_0      2.0      0.0      1.0
        class_1      0.0      0.0      0.0
        class_2      0.0      1.0      2.0
        >>> mc.generate_confusion_matrix(normalize=True)
                  0         1         2
        0  0.666667  0.000000  0.333333
        1  0.000000  0.000000  0.000000
        2  0.000000  0.333333  0.666667
        >>> mc.generate_confusion_matrix(with_labels=False)                                                                                                                                                                                                               
        array([[2., 0., 1.],
               [0., 0., 0.],
               [0., 1., 2.]])
        ```
        """

        check_scalar(normalize, 'normalize', bool)
        check_scalar(with_labels, 'with_labels', bool)
        check_scalar(labels, 'labels', (type(None), list, np.ndarray))

        matrix = self.__confusion_matrix.copy()

        if normalize:
            matrix = pd.DataFrame(norm(matrix, norm="l1"),
                                  index=matrix.index,
                                  columns=matrix.columns)

        if labels:
            check_consistent_length(labels, self.__labels)

            matrix.index = matrix.columns = labels

        matrix = matrix if with_labels else matrix.values

        return matrix

    def generate_metrics(self) -> dict:
        """Calculate and output metrics per class and overall accuracy.

        This method computes and outputs precision, recall, F1-score
        metrics per label and overall accuracy for all examples using
        *exact match ratio*.

        References
        ----------
        .. [1] `scikit-learn metrics module documentation
                <https://scikit-learn.org/stable/modules/classes.html#module-sklearn.metrics>`

        Returns
        -------
        report : dict
            Dictionary containg the precision, recall, F1-score metrics
            per label and overall accuracy for all examples.
            Confusion matrix whose i-th row and j-th column entry
            indicates the number of samples with true label being
            j-th class and predicted label beign i-th class.

        See also
        --------
        precision_score, recall_score, f1_score

        Examples
        --------
        ```python
        >>> from take_confusion_matrix import MetricsCalculation
        >>> labels = [0, 1, 2]
        >>> mc = MetricsCalculator(labels)
        >>> y_true = [2, 0, 2, 2, 0, 1]
        >>> y_pred = [0, 0, 2, 2, 0, 2]
        >>> mc.compute_matrix(y_true, y_pred)
        >>> mc.generate_metrics()
        {"0": {"precision": 0.6666666666666666,
            "recall": 1.0,
            "f1-score": 0.8},
        "1": {"precision": 0.0,
            "recall": 0.0,
            "f1-score": 0.0},
        "2": {"precision": 0.6666666666666666,
            "recall": 0.6666666666666666,
            "f1-score": 0.6666666666666666},
        "accuracy": 0.6666666666666666}
        ```
        """

        return self.___compute_metrics()

    def ___compute_metrics(self) -> dict:
        metrics = {str(label): {} for label in self.__labels}

        N = self.__confusion_matrix.sum().sum()
        total_tp = 0.

        for label in self.__labels:
            tp = self.__confusion_matrix[label][label]
            fn = self.__confusion_matrix[label].sum() - tp
            fp = self.__confusion_matrix.loc[label].sum() - tp
            tn = N - (tp + fn + fp)
            total_tp += tp

            label = str(label)
            metrics[label]["precision"] = self.__precision_score(tp, fp,
                                                                 tn, fn)
            metrics[label]["recall"] = self.__recall_score(tp, fp, tn, fn)
            metrics[label]["f1-score"] = self.__f1_score(tp, fp, tn, fn)

        metrics["accuracy"] = total_tp / N

        return metrics

    def __precision_score(self, tp: int, fp: int, tn: int, fn: int) -> float:
        """Calculate the precision.

        The precision is the ratio `tp / (tp + fp)` where `tp` is 
        the number of true positives and `fp` the number of false
        positives. The precision is intuitively the ability of the
        classifier not to label as positive a sample that is negative.

        The best value is 1 and the worst value is 0. 

        Parameters
        ----------
        tp : int 
            Number of true positives, which are the samples that were 
            correctly labeled as positive.

        fp : int 
            Number of false positives, which are the samples that were
            labeled positive but should have been labeled as negative.

        tn : int 
            Number of true negatives, which are the samples that were
            correctly labeled as negative.

        fn : int 
            Number of false negatives, which are the samples that were
            labeled as negative but should have been labeled as positive.

        Returns
        -------
        precision : float

        See also
        --------
        generate_metrics

        Examples
        --------
        ```python
        >>> from take_confusion_matrix import MetricsCalculation
        >>> labels = [0, 1, 2]
        >>> mc = MetricsCalculator(labels)
        >>> y_true = [2, 0, 2, 2, 0, 1]
        >>> y_pred = [0, 0, 2, 2, 0, 2]
        >>> mc.compute_matrix(y_true, y_pred)
        >>> mc.generate_metrics()
        {"0": {"precision": 0.6666666666666666,
            "recall": 1.0,
            "f1-score": 0.8},
        "1": {"precision": 0.0,
            "recall": 0.0,
            "f1-score": 0.0},
        "2": {"precision": 0.6666666666666666,
            "recall": 0.6666666666666666,
            "f1-score": 0.6666666666666666},
        "accuracy": 0.6666666666666666}
        ```
        """

        denominator = (tp + fp)

        return tp / denominator if denominator else 0.

    def __recall_score(self, tp: int, fp: int, tn: int, fn: int) -> float:
        """Calculate the recall.

        The recall is the ratio `tp / (tp + fn)` where `tp` is 
        the number of true positives and `fn` the number of false
        negatives. The recall is intuitively the ability of the
        classifier to find all the positive samples.

        The best value is 1 and the worst value is 0. 

        Parameters
        ----------
        tp : int 
            Number of true positives, which are the samples that were 
            correctly labeled as positive.

        fp : int 
            Number of false positives, which are the samples that were
            labeled positive but should have been labeled as negative.

        tn : int 
            Number of true negatives, which are the samples that were
            correctly labeled as negative.

        fn : int 
            Number of false negatives, which are the samples that were
            labeled as negative but should have been labeled as positive.

        Returns
        -------
        recall : float

        See also
        --------
        generate_metrics

        Examples
        --------
        ```python
        >>> from take_confusion_matrix import MetricsCalculation
        >>> labels = [0, 1, 2]
        >>> mc = MetricsCalculator(labels)
        >>> y_true = [2, 0, 2, 2, 0, 1]
        >>> y_pred = [0, 0, 2, 2, 0, 2]
        >>> mc.compute_matrix(y_true, y_pred)
        >>> mc.generate_metrics()
        {"0": {"precision": 0.6666666666666666,
            "recall": 1.0,
            "f1-score": 0.8},
        "1": {"precision": 0.0,
            "recall": 0.0,
            "f1-score": 0.0},
        "2": {"precision": 0.6666666666666666,
            "recall": 0.6666666666666666,
            "f1-score": 0.6666666666666666},
        "accuracy": 0.6666666666666666}
        ```
        """

        denominator = (tp + fn)

        return tp / denominator if denominator else 0.

    def __f1_score(self, tp: int, fp: int, tn: int, fn: int) -> float:
        """Calculate the F1 score, also known as balanced F-score or F-measure.

        The F1 score can be interpreted as a weighted average of the 
        precision and recall, where an F1 score reaches its best value 
        at 1 and worst score at 0. The relative contribution of precision 
        and recall to the F1 score are equal. 

        The formula for the F1 score is:

            F1 = 2 * (precision * recall) / (precision + recall)

        Parameters
        ----------
        tp : int 
            Number of true positives, which are the samples that were 
            correctly labeled as positive.

        fp : int 
            Number of false positives, which are the samples that were
            labeled positive but should have been labeled as negative.

        tn : int 
            Number of true negatives, which are the samples that were
            correctly labeled as negative.

        fn : int 
            Number of false negatives, which are the samples that were
            labeled as negative but should have been labeled as positive.

        Returns
        -------
        f1_score : float

        See also
        --------
        generate_metrics

        Examples
        --------
        ```python
        >>> from take_confusion_matrix import MetricsCalculation
        >>> labels = [0, 1, 2]
        >>> mc = MetricsCalculator(labels)
        >>> y_true = [2, 0, 2, 2, 0, 1]
        >>> y_pred = [0, 0, 2, 2, 0, 2]
        >>> mc.compute_matrix(y_true, y_pred)
        >>> mc.generate_metrics()
        {"0": {"precision": 0.6666666666666666,
            "recall": 1.0,
            "f1-score": 0.8},
        "1": {"precision": 0.0,
            "recall": 0.0,
            "f1-score": 0.0},
        "2": {"precision": 0.6666666666666666,
            "recall": 0.6666666666666666,
            "f1-score": 0.6666666666666666},
        "accuracy": 0.6666666666666666}
        """

        denominator = ((2.0 * tp) + fp + fn)

        return (2.0 * tp) / denominator if denominator else 0.
