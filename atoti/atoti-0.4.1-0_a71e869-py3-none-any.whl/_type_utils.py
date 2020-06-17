"""Utilities for types."""

from typing import Any, NewType

from typing_extensions import Literal

Port = NewType("Port", int)
ScenarioName = NewType("ScenarioName", str)
BASE_SCENARIO = ScenarioName("Base")

# pylint: disable=invalid-name
PercentileInterpolation = Literal["linear", "higher", "lower", "nearest", "midpoint"]
PercentileMode = Literal["simple", "centered", "inc", "exc"]
VarianceMode = Literal["sample", "population"]
# pylint: enable=invalid-name

# Something better can be done with typing.get_type_hints
# but we don't want to roll our own runtime type-checker just yet.
def check_literal(parameter: str, value: Any, expected_type: Any):
    """Check that the passed value matches the expected literals."""
    allowed_values = expected_type.__args__
    if value not in allowed_values:
        raise TypeError(
            f"the value of {parameter} must be one of {allowed_values}; got {value} instead"
        )
