import pytest

import numpy as np

from take_confusion_matrix import MetricsCalculator


def test_different_size_arrays_raises_value_error():
    mc = MetricsCalculator([0, 1])

    y_true = [0, 1, 0, 1]
    y_pred = [0, 0, 0, 0]

    mc.compute_matrix(y_true, y_pred)

    with pytest.raises(ValueError):
        mc.generate_confusion_matrix(labels=[1])


def test_different_size_labels_raises_value_error():
    mc = MetricsCalculator([0, 1])

    with pytest.raises(ValueError):
        mc.compute_matrix([0, 1], [0, 1, 2])


def test_different_type_arrays_raises_type_error():
    mc = MetricsCalculator([0, 1])

    with pytest.raises(TypeError):
        mc.compute_matrix(0, 0)


def test_different_type_labels_raises_type_error():
    with pytest.raises(TypeError):
        MetricsCalculator(0)


def test_different_type_labels_and_arrays_raises_type_error():
    mc = MetricsCalculator([0, 1])
    y_true = ["class_1", "class_1"]

    with pytest.raises(ValueError):
        mc.compute_matrix(y_true, y_true)


def test_labels_with_invalid_size_raises_value_error():
    with pytest.raises(ValueError):
        MetricsCalculator([])


def test_different_params_type_raises_type_error():
    mc = MetricsCalculator([0, 1])

    with pytest.raises(TypeError):
        mc.generate_confusion_matrix([])
        mc.generate_confusion_matrix(with_labels=[])
        mc.generate_confusion_matrix(labels=0)
