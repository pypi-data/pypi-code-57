from bson.binary import Binary
import numpy as np
import pickle as pkl

def from1d(array: np.ndarray) -> list:
    """Converts a NumPy ndarray to  a list object that can be stored in MongoDB

    Args:
        array (np.ndarray): [description]

    Returns:
        list: [description]
    """
    return array.tolist()

def from2d(array: np.ndarray) -> Binary:
    """[summary]

    Args:
        array (np.ndarray): [description]

    Returns:
        Binary: pickled binary representation of the 2d ndarray
    """
    return Binary(pkl.dumps(array, protocol=2), subtype=128)

def to1d(list: list) -> np.ndarray:
    """[summary]

    Args:
        list (list): [description]

    Returns:
        np.ndarray: ndarray representation of the list
    """
    return  np.fromiter(list)

def to2d(binary: Binary) -> np.ndarray:
    """[summary]

    Args:
        binary (Binary): [description]

    Returns:
        np.ndarray: ndarray representation of the pickled binary
    """
    return pkl.loads(binary)

def fromFloat(num: np.float) -> float:
    return float(num)

def fromInt(num: np.int) -> int:
    return int(num)
