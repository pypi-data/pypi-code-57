
from .list import ListLike

import numpy as np


class _Undefined:
    def __init__(self):
        pass


Undefined = _Undefined()
NoneType = type(None)

# TODO add NoneType (which contains Undefined)


# Create a numpy array of None
def nones(shape):
    """
    Create numpy array of None

    Parameters
    ----------
    shape : int or ListLike
        The shape of the array of Nones

    Returns
    -------
    numpy.ndarray
        Array of shape `shape` filled with None
    """

    if isinstance(shape, int):
        result = np.array([None] * shape)

    elif isinstance(shape, ListLike):
        result = np.array(np.repeat([None] * shape[0], shape[1]).reshape(*shape))

    else:
        raise AttributeError('shape %s unknown' % shape)

    return result
