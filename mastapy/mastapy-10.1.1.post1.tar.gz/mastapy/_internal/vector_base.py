'''vector_base.py'''


from typing import Tuple, List, Union, Iterable, Iterator
from abc import ABC, abstractmethod

import numpy as np


NUM = Union[float, int]
ERROR_COMP_MESSAGE = (
    'Vectors must have equal number of '
    'dimensions for comparison.')
ERROR_SET_MESSAGE = (
    'Can only set a vector to a '
    'number or an iterable of numbers.')
ERROR_COMP_ELEM_MESSAGE = (
    'Can only compare a vector to a '
    'number or an iterable of numbers.')
ERROR_SET_ELEM_MESSAGE = (
    'Can only set elements of a vector to a '
    'number or an iterable of numbers.')
ERROR_SET_PROPERTY = (
    'Can not set individual components. Try setting the property '
    'directly instead.')


class VectorException(Exception):
    '''VectorException

    Exception raised for errors occurring in the Vector3D class.
    '''


class VectorBase(ABC):
    '''VectorBase

    Abstract Base Class for all vector types.
    '''

    def __init__(self, values: List[float]):
        self._values = values

    def _iter_conv_comp(self, iterable: Iterable[NUM]) -> Tuple[NUM]:
        values = tuple(float(v) for v in iterable)
        if len(values) != len(self):
            raise VectorException(ERROR_COMP_MESSAGE)
        return values

    def _iter_conv_set(
            self, iterable: Iterable[NUM], length: int) -> Tuple[NUM]:
        values = tuple(float(v) for v in iterable)
        if len(values) != length:
            raise VectorException(ERROR_SET_MESSAGE)
        return values

    @classmethod
    @abstractmethod
    def broadcast(cls, value: float) -> 'VectorBase':
        pass

    @classmethod
    @abstractmethod
    def from_tuple(cls, t: Tuple) -> 'VectorBase':
        pass

    @abstractmethod
    def __add__(self, other) -> 'VectorBase':
        pass

    @abstractmethod
    def __sub__(self, other) -> 'VectorBase':
        pass

    @abstractmethod
    def __mul__(self, other) -> 'VectorBase':
        pass

    @abstractmethod
    def __truediv__(self, other) -> 'VectorBase':
        pass

    @abstractmethod
    def __floordiv__(self, other) -> 'VectorBase':
        pass

    def __len__(self) -> int:
        return len(self._values)

    def __contains__(self, value: object) -> bool:
        return value in self._values

    def __getitem__(self, index: Union[int, slice]) -> float:
        return self._values[index]

    def __setitem__(
            self, index: Union[int, slice],
            value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                self._values[index] = [float(x) for x in value]
            else:
                self._values[index] = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_ELEM_MESSAGE)

    def __iter__(self) -> Iterator[float]:
        return iter(self._values)

    def __lt__(self, value: Union[NUM, Iterable[NUM]]) -> bool:
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_comp(value)
                return all(
                    map(lambda t: t[0] < t[1], zip(self._values, values)))
            else:
                value = float(value)
                return all(map(lambda x: x < value, self._values))
        except ValueError:
            raise VectorException(ERROR_COMP_MESSAGE)

    def __le__(self, value: Union[NUM, Iterable[NUM]]) -> bool:
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_comp(value)
                return all(
                    map(lambda t: t[0] <= t[1], zip(self._values, values)))
            else:
                value = float(value)
                return all(map(lambda x: x <= value, self._values))
        except ValueError:
            raise VectorException()

    def __gt__(self, value: Union[NUM, Iterable[NUM]]) -> bool:
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_comp(value)
                return all(
                    map(lambda t: t[0] > t[1], zip(self._values, values)))
            else:
                value = float(value)
                return all(map(lambda x: x > value, self._values))
        except ValueError:
            raise VectorException(ERROR_COMP_ELEM_MESSAGE)

    def __ge__(self, value: Union[NUM, Iterable[NUM]]) -> bool:
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_comp(value)
                return all(
                    map(lambda t: t[0] >= t[1], zip(self._values, values)))
            else:
                value = float(value)
                return all(map(lambda x: x >= value, self._values))
        except ValueError:
            raise VectorException(ERROR_COMP_ELEM_MESSAGE)

    def __str__(self) -> str:
        return '({})'.format(', '.join((str(x) for x in self._values)))

    def __repr__(self) -> str:
        return '{}({})'.format(
            self.__class__.__qualname__, ', '.join(
                (str(x) for x in self._values)))
