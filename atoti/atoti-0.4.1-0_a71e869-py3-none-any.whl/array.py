"""Functions operating on array measures."""

from __future__ import annotations

from typing import Union

from ._docs_utils import (
    QUANTILE_DOC,
    STD_AND_VAR_DOC,
    STD_DOC_KWARGS,
    VAR_DOC_KWARGS,
    doc,
)
from ._functions.measure import sqrt
from ._measures.calculated_measure import CalculatedMeasure, Operator
from ._measures.quantile_measure import QuantileMeasure
from ._type_utils import (
    PercentileInterpolation,
    PercentileMode,
    VarianceMode,
    check_literal,
)
from .measure import Measure, _convert_to_measure


def sum(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the sum of all the elements of the passed array measure."""
    return CalculatedMeasure(Operator("sum_vector", [measure]))


def positive_values(measure: Measure) -> Measure:
    """Return a measure where all the elements < 0 of the passed array measure are replaced by 0."""
    return CalculatedMeasure(Operator("positive_vector", [measure]))


def negative_values(measure: Measure) -> Measure:
    """Return a measure where all the elements > 0 of the passed array measure are replaced by 0."""
    return CalculatedMeasure(Operator("negative_vector", [measure]))


def mean(measure: Measure) -> Measure:
    """Return a measure equal to the mean of all the elements of the passed array measure."""
    return CalculatedMeasure(Operator("mean_vector", [measure]))


def min(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the minimum element of the passed array measure."""
    return CalculatedMeasure(Operator("min_vector", [measure]))


def max(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the maximum element of the passed array measure."""
    return CalculatedMeasure(Operator("max_vector", [measure]))


_QUANTILE_STD_AND_VAR_DOC_KWARGS = {
    "what": "of the elements of the passed array measure"
}


@doc(STD_AND_VAR_DOC, **{**VAR_DOC_KWARGS, **_QUANTILE_STD_AND_VAR_DOC_KWARGS})
def var(measure: Measure, *, mode: VarianceMode = "sample") -> Measure:
    check_literal("mode", mode, VarianceMode)
    return CalculatedMeasure(Operator("variance", [measure, mode]))


@doc(
    STD_AND_VAR_DOC, **{**STD_DOC_KWARGS, **_QUANTILE_STD_AND_VAR_DOC_KWARGS},
)
def std(measure: Measure, *, mode: VarianceMode = "sample") -> Measure:
    check_literal("mode", mode, VarianceMode)
    return sqrt(var(measure, mode=mode))


def sort(measure: Measure) -> Measure:
    """Return an array measure with the elements of the passed array measure sorted."""
    return CalculatedMeasure(Operator("sort", [measure]))


@doc(QUANTILE_DOC, **_QUANTILE_STD_AND_VAR_DOC_KWARGS)
def quantile(
    measure: Measure,
    q: Union[float, Measure],
    *,
    mode: PercentileMode = "inc",
    interpolation: PercentileInterpolation = "linear",
) -> Measure:
    if isinstance(q, float):
        if q < 0 or q > 1:
            raise ValueError("Quantile must be between 0 and 1.")
    elif not isinstance(q, Measure):
        raise TypeError("The quantile must be a measure or a float.")

    return QuantileMeasure([measure, _convert_to_measure(q)], mode, interpolation)


def n_lowest(measure: Measure, n: Union[int, Measure]) -> Measure:
    """Return an array measure containing the ``n`` lowest elements of the passed array measure."""
    if isinstance(n, int):
        if n <= 0:
            raise ValueError("n must be greater than 0.")
    elif not isinstance(n, Measure):
        raise TypeError("n must be a measure or an int.")
    return CalculatedMeasure(Operator("n_lowest", [measure, _convert_to_measure(n)]))


def nth_lowest(measure: Measure, n: Union[int, Measure]) -> Measure:
    """Return a measure equal to the ``n``-th lowest element of the passed array measure."""
    if isinstance(n, int):
        if n <= 0:
            raise ValueError("n must be greater than 0.")
    elif not isinstance(n, Measure):
        raise TypeError("n must be a measure or an int.")
    return CalculatedMeasure(Operator("nth_lowest", [measure, _convert_to_measure(n)]))


def n_greatest(measure: Measure, n: Union[int, Measure]) -> Measure:
    """Return an array measure containing the ``n`` greatest elements of the passed array measure."""
    if isinstance(n, int):
        if n <= 0:
            raise ValueError("n must be greater than 0.")
    elif not isinstance(n, Measure):
        raise TypeError("n must be a measure or an int.")
    return CalculatedMeasure(Operator("n_greatest", [measure, _convert_to_measure(n)]))


def nth_greatest(measure: Measure, n: Union[int, Measure]) -> Measure:
    """Return a measure equal to the ``n``-th greatest element of the passed array measure."""
    if isinstance(n, int):
        if n <= 0:
            raise ValueError("n must be greater than 0.")
    elif not isinstance(n, Measure):
        raise TypeError("n must be a measure or an int.")
    return CalculatedMeasure(
        Operator("nth_greatest", [measure, _convert_to_measure(n)])
    )


def len(measure: Measure) -> Measure:  # pylint: disable=redefined-builtin
    """Return a measure equal to the number of elements of the passed array measure."""
    return CalculatedMeasure(Operator("vector_length", [measure]))


def prefix_sum(measure: Measure) -> Measure:
    """Return a measure equal to the sum of the previous elements in the passed array measure.

    Example:
        If an array has the following values: ``[2.0, 1.0, 0.0, 3.0]``,
        the returned array will be: ``[2.0, 3.0, 3.0, 6.0]``.
    """
    return CalculatedMeasure(Operator("prefix_sum", [measure]))
