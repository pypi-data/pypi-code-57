import operator

import numpy as np

from typing import (Any, Callable, Dict, Mapping, List, Tuple, Optional, Union,
                    Iterable, Iterator)


TAFRA_TYPE: Dict[str, Callable[[np.ndarray], np.ndarray]] = {
    'int': lambda x: x.astype(int),
    'float': lambda x: x.astype(float),
    'bool': lambda x: x.astype(bool),
    'str': lambda x: x.astype(str),
    'date': lambda x: x.astype('datetime64'),
    'object': lambda x: x.astype(object),
}

RECORD_TYPE: Dict[str, Callable[[Any], Any]] = {
    'int': lambda x: int(x),
    'float': lambda x: float(x),
    'bool': lambda x: bool(x),
    'str': lambda x: str(x),
    'date': lambda x: x.strftime(r'%Y-%m-%d'),
    'object': lambda x: str(x),
}

JOIN_OPS: Dict[str, Callable[[Any, Any], Any]] = {
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge
}


# for the passed argument to an aggregation
InitAggregation = Mapping[
    str,
    Union[
        Callable[[np.ndarray], Any],
        Tuple[Callable[[np.ndarray], Any], str]
    ]
]


# for the result type of IterateBy
GroupDescription = Tuple[
    Tuple[Any, ...],  # tuple of unique values from group-by columns
    np.ndarray,  # int array of row indices into original tafra for this group
    'Tafra'  # sub-tafra for the group
]

# Import here to resolve circular dependency
# from .base import Tafra
