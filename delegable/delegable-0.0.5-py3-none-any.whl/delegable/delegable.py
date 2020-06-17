"""
Convenient classes to enable delegate
"""
import copy
import inspect
import logging as log
from typing import Sequence, Any, Dict, Tuple, Callable, Union


def delegator(cls):
    """
    A decorator for class, which delegates its functions to a decolated class
    """
    def _new(func):
        def _wrap(cls, *args, **kwargs):
            instance = func(cls)
            instance._delegates = {}
            return instance
        return _wrap

    def _getattr(self, name) -> Any:
        """
        Look for delegated funcion

        If any found, raises AttributeError.
        """
        log.debug('delegates={}'.format(self._delegates))
        for to, funcs in self._delegates.items():
            funcs = (funcs,) if type(funcs) is str else funcs
            for func in funcs:
                # Check if func is in any of the delegates
                if name == func and hasattr(getattr(self, to), func):
                    # Delegate the call
                    return getattr(getattr(self, to), func)
        raise AttributeError("'{}' object has no attribute '{}'".format(type(self).__name__, name))

    def _delegate(self, *funcs, to: str) -> Sequence:
        """ Update delegates for delegated object specified by `to` """
        self._delegates.update({to: funcs})
        return self._delegates

    def _get_delegates(self):
        """ getter of delegates """
        return self._delegates

    def _set_delegates(self, delegates):
        """ setter of delegates """
        self._delegates = delegates
        return self._delegates

    cls.__new__ = _new(cls.__new__)
    cls.__getattr__ = _getattr
    cls.delegate = _delegate
    cls.delegates = property(_get_delegates, _set_delegates)
    return cls
