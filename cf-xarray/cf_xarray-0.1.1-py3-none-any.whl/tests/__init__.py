import re
from contextlib import contextmanager

import dask
import pytest


@contextmanager
def raises_regex(error, pattern):
    __tracebackhide__ = True
    with pytest.raises(error) as excinfo:
        yield
    message = str(excinfo.value)
    if not re.search(pattern, message):
        raise AssertionError(
            f"exception {excinfo.value!r} did not match pattern {pattern!r}"
        )


class CountingScheduler:
    """ Simple dask scheduler counting the number of computes.

    Reference: https://stackoverflow.com/questions/53289286/ """

    def __init__(self, max_computes=0):
        self.total_computes = 0
        self.max_computes = max_computes

    def __call__(self, dsk, keys, **kwargs):
        self.total_computes += 1
        if self.total_computes > self.max_computes:
            raise RuntimeError(
                "Too many computes. Total: %d > max: %d."
                % (self.total_computes, self.max_computes)
            )
        return dask.get(dsk, keys, **kwargs)


def raise_if_dask_computes(max_computes=0):
    scheduler = CountingScheduler(max_computes)
    return dask.config.set(scheduler=scheduler)
