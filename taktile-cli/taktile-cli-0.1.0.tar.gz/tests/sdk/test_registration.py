import numpy as np
import pandas as pd
import pytest

from tktl import Tktl
from tktl.core.exceptions.exceptions import ValidationException


@pytest.mark.parametrize(
    "X,y",
    [
        (pd.DataFrame({"a": [1, 2, 3]}), pd.Series([4, 5, 5])),  # pandas
        ({"a": [1, 2, 3]}, [4, 5, 5]),  # base
    ],
)
def test_creation(X, y):
    tktl = Tktl()

    @tktl.endpoint(X=X, y=y, kind="regression")
    def predict(X):
        return [0] * len(X)

    endpoint = tktl.endpoints[0]
    assert type(endpoint.X) == pd.DataFrame
    assert type(endpoint.y) == pd.Series
    assert endpoint.y.name == "Outcome"
    assert endpoint.func(pd.DataFrame(X)) == [0, 0, 0]


def test_validate_func():
    with pytest.raises(ValidationException):
        tktl = Tktl()
        X = {"a": [1, 2, 3]}
        y = [4, 5, 5]

        @tktl.endpoint(X=X, y=y)
        def predict(X):
            return [0] * (len(X) - 1)


def test_input_dimensions():
    with pytest.raises(ValidationException):
        tktl = Tktl()
        X = {"a": [1, 2, 3]}
        y = [4, 5]

        @tktl.endpoint(X=X, y=y)
        def predict(X):
            return [0] * len(X)


def test_func_dimensions():
    with pytest.raises(ValidationException):
        tktl = Tktl()
        X = {"a": [1, 2, 3]}
        y = [4, 5, 5]

        @tktl.endpoint(X=X, y=y)
        def predict(X):
            return [0] * (len(X) - 1)


def test_unknown_kind():
    with pytest.raises(NotImplementedError):
        tktl = Tktl()
        X = {"a": [1, 2, 3]}
        y = [4, 5, 5]

        @tktl.endpoint(X=X, y=y, kind="unknown kind")
        def predict(X):
            return [0] * len(X)


def test_missing():
    tktl = Tktl()
    X = {"a": [1, 2, 3]}
    y = pd.Series([0.1, 0.2, None])

    with pytest.warns(UserWarning):

        @tktl.endpoint(X=X, y=y, kind="regression")
        def predict(X):
            return [0] * len(X)


def test_numpy_arrays():
    tktl = Tktl()
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    y = np.array([0.1, 0.2, 0.3])

    @tktl.endpoint(X=X, y=y, kind="regression")
    def predict(X):
        return np.array([0] * len(X))

    endpoint = tktl.endpoints[0]
    assert type(endpoint.X) == pd.DataFrame
    assert type(endpoint.y) == pd.Series
    assert endpoint.y.name == "Outcome"
    assert np.allclose(endpoint.func(pd.DataFrame(X)), np.array([0, 0, 0]))
