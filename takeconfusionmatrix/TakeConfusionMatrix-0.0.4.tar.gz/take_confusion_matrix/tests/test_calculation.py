import pytest

import numpy as np

from take_confusion_matrix import MetricsCalculator


def test_matrix_for_two_unchaging_labels_returns_expected_results():
    labels = [0, 1]

    mc = MetricsCalculator(labels)

    y_true = [0, 1, 0, 1]
    y_pred = [0, 0, 0, 0]

    mc.compute_matrix(y_true, y_pred)

    expected_matrix = [[2, 2],
                       [0, 0]]
    actual_matrix = mc.generate_confusion_matrix().values

    assert (expected_matrix == actual_matrix).all()


def test_matrix_for_three_unchanging_labels_returns_expected_results():
    labels = [0, 1, 2]

    mc = MetricsCalculator(labels)

    y_true = [2, 0, 2, 2, 0, 1]
    y_pred = [0, 0, 2, 2, 0, 2]

    mc.compute_matrix(y_true, y_pred)

    expected_matrix = [[2, 0, 1],
                       [0, 0, 0],
                       [0, 1, 2]]
    actual_matrix = mc.generate_confusion_matrix().values

    assert (expected_matrix == actual_matrix).all()


def test_matrix_for_three_changing_labels_returns_expected_results():
    labels = [0, 1, 2]

    mc = MetricsCalculator(labels)

    y_true = [0, 1, 0, 1]
    y_pred = [0, 0, 0, 0]

    mc.compute_matrix(y_true, y_pred)

    y_true = [0, 2, 0, 2]
    y_pred = [0, 0, 0, 0]

    mc.compute_matrix(y_true, y_pred)

    expected_matrix = [[4, 2, 2],
                       [0, 0, 0],
                       [0, 0, 0]]
    actual_matrix = mc.generate_confusion_matrix().values

    assert (expected_matrix == actual_matrix).all()


def test_matrix_batched_computation_returns_expected_results():
    labels = [0, 1, 2]

    mc = MetricsCalculator(labels)

    times = 10

    y_true = [2, 0, 2, 2, 0, 1]
    y_pred = [0, 0, 2, 2, 0, 2]

    for i in range(times):
        mc.compute_matrix(y_true, y_pred)

    expected_matrix = [[2 * times, 0,         1 * times],
                       [0,         0,         0],
                       [0,         1 * times, 2 * times]]
    actual_matrix = mc.generate_confusion_matrix().values

    assert (expected_matrix == actual_matrix).all()


def test_diagonal_matrix_computation_returns_expected_results():
    labels = [0, 1, 2]

    mc = MetricsCalculator(labels)

    times = 10

    y_true = [0, 0, 1, 1, 2, 2]
    y_pred = [0, 0, 1, 1, 2, 2]

    for i in range(times):
        mc.compute_matrix(y_true, y_pred)

    expected_matrix = [[2 * times, 0,         0],
                       [0,         2 * times, 0],
                       [0,         0,         2 * times]]
    actual_matrix = mc.generate_confusion_matrix().values

    assert (expected_matrix == actual_matrix).all()


def test_string_labels_matrix_computation_returns_expected_results():
    labels = ["class_0", "class_1"]

    mc = MetricsCalculator(labels)

    y_true = ["class_0", "class_1", "class_0", "class_1"]
    y_pred = ["class_0", "class_0", "class_0", "class_0"]

    mc.compute_matrix(y_true, y_pred)

    expected_matrix = [[2, 2],
                       [0, 0]]
    actual_matrix = mc.generate_confusion_matrix().values

    assert (expected_matrix == actual_matrix).all()


def test_matrix_with_user_specified_labels_retuns_uses_labels():
    labels = [0, 1]

    mc = MetricsCalculator(labels)

    y_true = [0, 1, 0, 1]
    y_pred = [0, 0, 0, 0]

    mc.compute_matrix(y_true, y_pred)

    labels = ["class_0", "class_1"]
    matrix = mc.generate_confusion_matrix(labels=labels)

    assert (matrix.index.values == labels).all()
    assert (matrix.columns == labels).all()
    assert matrix["class_0"]["class_0"] == 2


def test_matrix_without_labels_returns_ndarray():
    labels = [0, 1]

    mc = MetricsCalculator(labels)

    y_true = [0, 1, 0, 1]
    y_pred = [0, 0, 0, 0]

    mc.compute_matrix(y_true, y_pred)

    matrix = mc.generate_confusion_matrix(with_labels=False)

    assert isinstance(matrix, np.ndarray)


def test_metrics_computation_returns_expected_results():
    labels = [0, 1, 2]

    mc = MetricsCalculator(labels)

    y_true = [2, 0, 2, 2, 0, 1]
    y_pred = [0, 0, 2, 2, 0, 2]

    mc.compute_matrix(y_true, y_pred)

    expected_dict = {"0": {"precision": 0.6666666666666666,
                           "recall": 1.0,
                           "f1-score": 0.8},
                     "1": {"precision": 0.0,
                           "recall": 0.0,
                           "f1-score": 0.0},
                     "2": {"precision": 0.6666666666666666,
                           "recall": 0.6666666666666666,
                           "f1-score": 0.6666666666666666},
                     "accuracy": 0.6666666666666666}
    actual_metrics = mc.generate_metrics()

    assert actual_metrics == expected_dict


def test_matrix_returns_normalized_results():
    labels = [0, 1, 2]

    mc = MetricsCalculator(labels)

    y_true = [2, 0, 2, 2, 0, 1]
    y_pred = [0, 0, 2, 2, 0, 2]

    mc.compute_matrix(y_true, y_pred)

    expected_matrix = [[0.66666667, 0.,         0.33333333],
                       [0.,         0.,         0.],
                       [0.,         0.33333333, 0.66666667]]
    actual_matrix = mc.generate_confusion_matrix(normalize=True,
                                                 with_labels=False)

    assert expected_matrix == pytest.approx(actual_matrix)
