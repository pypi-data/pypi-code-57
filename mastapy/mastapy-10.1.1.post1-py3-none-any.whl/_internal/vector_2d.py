'''vector_2d.py'''

from typing import Tuple, Union, Iterable

import numpy as np

from mastapy._internal.vector_base import (
    VectorBase, VectorException, NUM, ERROR_SET_MESSAGE,
    ERROR_SET_PROPERTY)


__all__ = ('Vector2D',)


class Vector2D(VectorBase):
    ''' Create a Vector2D from X and Y components

    Custom Python Vector2D class. The class derives from tuple and can
    therefore be used like a tuple, but with additional operations.
    Internally uses NumPy for mathematical operations.

    Args:
        x: NUM
        y: NUM

    Returns:
        Vector2D
    '''

    def __init__(self, x: NUM, y: NUM) -> 'Vector2D':
        self.wrapped = None
        super().__init__([float(x), float(y)])

    @classmethod
    def broadcast(cls, value: NUM) -> 'Vector2D':
        ''' Create a Vector2D by broadcasting a value to all of its dimensions

        Args:
            value: NUM

        Returns:
            Vector2D
        '''

        return cls(value, value)

    @classmethod
    def from_tuple(cls, t: Tuple[NUM, NUM]) -> 'Vector2D':
        ''' Create a Vector2D from another tuple

        Args:
            t: Tuple[NUM, NUM]

        Returns:
            Vector2D
        '''

        try:
            return cls(t[0], t[1])
        except (KeyError, TypeError, AttributeError):
            raise VectorException('Tuple must be of at least length 2.')

    @property
    def x(self) -> float:
        ''' Get the X component of the vector

        Returns:
            float
        '''

        return self[0]

    @x.setter
    def x(self, value: NUM):
        self[0] = float(value)
        if self.wrapped:
            raise VectorException(ERROR_SET_PROPERTY)

    @property
    def y(self) -> float:
        ''' Get the Y component of the vector

        Returns:
            float
        '''

        return self[1]

    @y.setter
    def y(self, value: NUM):
        self[1] = float(value)
        if self.wrapped:
            raise VectorException(ERROR_SET_PROPERTY)

    @property
    def xx(self) -> 'Vector2D':
        ''' Get the XX components of the vector

        Returns:
            Vector2D
        '''

        return Vector2D.broadcast(self.x)

    @property
    def xy(self) -> 'Vector2D':
        ''' Get the XY components of the vector

        Returns:
            Vector2D
        '''

        return Vector2D(self.x, self.y)

    @xy.setter
    def xy(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 2)
                self.x = values[0]
                self.y = values[1]
            else:
                self.x = self.y = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def yx(self) -> 'Vector2D':
        ''' Get the YX components of the vector

        Returns:
            Vector2D
        '''

        return Vector2D(self.y, self.x)

    @yx.setter
    def yx(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 2)
                self.y = values[0]
                self.x = values[1]
            else:
                self.y = self.x = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def yy(self) -> 'Vector2D':
        ''' Get the YY components of the vector

        Returns:
            Vector2D
        '''

        return Vector2D.broadcast(self.y)

    def __add__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector2D':
        return Vector2D.from_tuple(np.add(self, other))

    def __radd__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector2D':
        return Vector2D.from_tuple(np.add(other, self))

    def __sub__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector2D':
        return Vector2D.from_tuple(np.subtract(self, other))

    def __rsub__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector2D':
        return Vector2D.from_tuple(np.subtract(other, self))

    def __mul__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector2D':
        return Vector2D.from_tuple(np.multiply(self, other))

    def __rmul__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector2D':
        return Vector2D.from_tuple(np.multiply(other, self))

    def __truediv__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector2D':
        return Vector2D.from_tuple(np.divide(self, other))

    def __rtruediv__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector2D':
        return Vector2D.from_tuple(np.divide(other, self))

    def __floordiv__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector2D':
        return Vector2D.from_tuple(np.floor_divide(self, other))

    def __rfloordiv__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector2D':
        return Vector2D.from_tuple(np.floor_divide(other, self))
