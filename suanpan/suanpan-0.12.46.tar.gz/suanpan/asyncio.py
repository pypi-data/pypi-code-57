# coding=utf-8
from __future__ import absolute_import, print_function

import gevent
import gevent.monkey

from suanpan.utils import pbar as spbar

gevent.monkey.patch_all(thread=False)


def imap(func, iterable, timeout=None, count=None, pbar=None):
    return iwait(
        [gevent.spawn(func, i) for i in iterable],
        timeout=timeout,
        count=count,
        pbar=pbar,
    )


def map(func, iterable, timeout=None, count=None, pbar=None):
    return list(imap(func, iterable, timeout=timeout, count=count, pbar=pbar))


def istarmap(func, iterable, timeout=None, count=None, pbar=None):
    return iwait(
        [gevent.spawn(func, *i) for i in iterable],
        timeout=timeout,
        count=count,
        pbar=pbar,
    )


def starmap(func, iterable, timeout=None, count=None, pbar=None):
    return list(istarmap(func, iterable, timeout=timeout, count=count, pbar=pbar))


def run(funcs, *args, **kwargs):
    return [gevent.spawn(func, *args, **kwargs) for func in funcs]


def wait(objects, timeout=None, count=None, pbar=None):
    return list(iwait(objects, timeout=timeout, count=count, pbar=pbar))


def iwait(iterable, timeout=None, count=None, pbar=None):
    iterable, total = spbar.getIterableLen(iterable, config=pbar, total=count)
    iterable = _iwait(iterable, timeout=timeout, count=count)
    return spbar.one(iterable, config=pbar, total=total)


def _iwait(objects, timeout=None, count=None):
    for obj in gevent.iwait(objects, timeout=timeout, count=count):
        if getattr(obj, "exception", None) is not None:
            if hasattr(obj, "_raise_exception"):
                obj._raise_exception()  # pylint: disable=protected-access
            else:
                raise obj.exception
        yield obj


def sleep(seconds=0, ref=True):
    return gevent.sleep(seconds=seconds, ref=ref)


def switch():
    return sleep(0)


def kill(iterable, exception=gevent.GreenletExit, block=True, timeout=None):
    iterable = iterable if isinstance(iterable, (list, tuple)) else [iterable]
    return gevent.killall(iterable, exception=exception, block=block, timeout=timeout)


def current():
    return gevent.getcurrent()
