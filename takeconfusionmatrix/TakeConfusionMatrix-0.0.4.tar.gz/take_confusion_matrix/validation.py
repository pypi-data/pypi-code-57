import numpy as np


def check_value_mapped(mapper: dict, values):
    """Check that all values passed were mapped

    Checks whether the values passed were previously mapped.

    Parameters
    ----------
    mapper : dict
        Dictionary with the values previously mapped.

    values : 1d array-like
        Values to be validated.

    Raises
    -------
    ValueError
        If the parameter's value violates the given bounds.
    """

    for value in values:
        if not mapper.get(value, False):
            raise ValueError(f"Found value `{value}` while "
                             f"the expected ones were {list(mapper.keys())}.")


def check_array_size(x: object, name: str, min_size: [int, float]):
    """Validate scalar parameter size.

    Parameters
    ----------
    x : object
        The scalar parameter to validate.

    name : str
        The name of the parameter to be printed in error messages.

    min_size : int or float
        The minimum valid size the parameter can take. 

    Raises
    -------
    TypeError
        If the parameter's type does not match the desired type.

    ValueError
        If the parameter's value violates the given bounds.
    """
    size = len(x)
    if size < min_size:
        raise ValueError(f"Size of `{name}` = {size}"
                         f", must be >= {min_size}")
