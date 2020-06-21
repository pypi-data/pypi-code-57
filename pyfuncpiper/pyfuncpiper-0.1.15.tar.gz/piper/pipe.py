from typing import Callable, Sequence
from functools import reduce

__all__ = ['pipe']


def pipe(*fns: Sequence[Callable]) -> Callable:
    def reduce_apply(initial_arg):
        def reduce_callback(fn_value, fn):
            return fn(fn_value)

        return reduce(
            reduce_callback,
            fns,
            initial_arg
        )

    return reduce_apply
