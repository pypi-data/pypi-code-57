from dataclasses import dataclass
import functools
import warnings
from typing import Callable

import pandas as pd

from tktl.core.exceptions import exceptions


@dataclass
class Endpoint:
    """Container for endpoint components"""

    func: Callable
    kind: str
    X: pd.DataFrame
    y: pd.Series


class Tktl:
    def __init__(self):
        self.endpoints = []

    # This is the user-facing decorator for function registration
    def endpoint(
        self,
        func: Callable = None,
        X: pd.DataFrame = None,
        y: pd.Series = None,
        kind: str = "regression",
    ):
        """Register function as a Taktile endpoint

        Parameters
        ----------
        func : Callable, optional
            Function that describes the desired operation, by default None
        X : pd.DataFrame, optional
            Reference input dataset for testing func, by default None
        y : pd.Series, optional
            Reference output for evaluating func, by default None
        kind : str, optional
            Specification of endpoint type ("regression", "binary"), by default "regression"

        Returns
        -------
        Callable
            Wrapped function
        """
        if func is None:
            return functools.partial(self.endpoint, kind=kind, X=X, y=y)

        X, y = self._convert_xy(X, y, kind=kind)
        self._validate_func(func, X, y)
        endpoint = Endpoint(func, kind, X=X, y=y)
        self.endpoints.append(endpoint)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            pred = func(*args, **kwargs)
            return pred

        return wrapper

    def _convert_xy(self, X, y, kind):
        # Convert X to DataFrame
        try:
            X = pd.DataFrame(X)
        except ValueError:
            raise exceptions.ConversionException(
                "Could not convert X to pandas dataframe"
            )

        if len(X) > 1e6:
            warnings.warn(
                f"X is very large (N={len(X)}). "
                f"Please consider using a smaller reference dataset."
            )

        # Convert y to Series
        try:
            y = pd.Series(y)
            y.name = y.name or "Outcome"

            if kind == "regression":
                y = y.astype(float)
            elif kind == "binary":
                y = y.astype(bool)
            else:
                raise NotImplementedError(f"Unknown endpoint kind: {kind}")

        except ValueError:
            raise exceptions.ConversionException("Could not convert y to pandas series")

        # Drop observations with missing outcomes
        id_missing = y.isna()
        n_missing = id_missing.sum()
        if id_missing.sum() > 0:
            warnings.warn(f"y contains {n_missing} missing values that will be dropped")
            X = X.loc[~id_missing]
            y = y.loc[~id_missing]

        if y.shape != (len(X),):
            raise exceptions.ValidationException("y is inconsistent with input data X")

        return X, y

    def _validate_func(self, func, X, y):
        pred = func(X)
        try:
            pred = list(pred)
        except ValueError:
            raise exceptions.ConversionException(
                "Could not convert function output to list"
            )

        if len(pred) != len(X):
            raise exceptions.ValidationException(
                "Predictions are inconsistent with input data X"
            )
