"""result_type
"""
from functools import reduce

import torch


def result_type(type_examples):
    """Get result type with torch.result_type

    Args:
        type_examples (tensor): list of example objects
    """
    def get_result(x_1, x_2):
        args = [x_1, x_2]
        required_type = torch.result_type(*args)
        return list(filter(lambda arg: arg.dtype == required_type, args))[0]
    # pylint: disable=unnecessary-lambda
    return reduce(lambda x, y: get_result(x, y), type_examples)[0].dtype
