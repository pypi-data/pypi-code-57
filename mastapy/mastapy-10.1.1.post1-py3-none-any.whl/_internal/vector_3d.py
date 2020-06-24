'''vector_3d.py'''


from typing import Tuple, Union, Iterable, Any

import numpy as np

from mastapy._internal.vector_base import (
    VectorException, NUM, ERROR_SET_MESSAGE,
    ERROR_SET_PROPERTY)
from mastapy._internal.vector_2d import Vector2D


__all__ = ('Vector3D',)


class Vector3D(Vector2D):
    '''Create a Vector3D from X, Y and Z components

    Custom Python implementation of Masta API's Vector3D class. The class
    derives from tuple and can therefore be used like a tuple, but with
    additional operations. Internally uses NumPy for mathematical
    operations.

    Args:
        x: NUM
        y: NUM
        z: NUM

    Returns:
        Vector3D
    '''

    def __init__(self, x: NUM, y: NUM, z: NUM) -> 'Vector3D':
        self.wrapped = None
        super(Vector2D, self).__init__([float(x), float(y), float(z)])

    @classmethod
    def broadcast(cls, value: NUM) -> 'Vector3D':
        ''' Create a Vector3D by broadcasting a value to all of its dimensions

        Args:
            value: NUM

        Returns:
            Vector3D
        '''

        return cls(value, value, value)

    @classmethod
    def from_tuple(cls, t: Tuple[NUM, NUM, NUM]) -> 'Vector3D':
        ''' Create a Vector3D from another tuple

        Args:
            t: Tuple[NUM, NUM, NUM]

        Returns:
            Vector3D
        '''

        try:
            return cls(t[0], t[1], t[2])
        except (KeyError, TypeError, AttributeError):
            raise VectorException('Tuple must be of at least length 3.')

    @classmethod
    def wrap(cls, value: Any) -> 'Vector3D':
        try:
            new_vector = cls(value.X, value.Y, value.Z)
            new_vector.wrapped = value
            return new_vector
        except AttributeError:
            raise VectorException('Value to wrap has no X, Y or Z component.')

    @property
    def z(self) -> float:
        ''' Get the Z component of the vector

        Returns:
            float
        '''

        return self[2]

    @z.setter
    def z(self, value: NUM):
        self[2] = float(value)
        if self.wrapped:
            raise VectorException(ERROR_SET_PROPERTY)

    @property
    def xz(self) -> Vector2D:
        ''' Get the XZ components of the vector

        Returns:
            Vector2D
        '''

        return Vector2D(self.x, self.z)

    @xz.setter
    def xz(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 2)
                self.x = values[0]
                self.z = values[1]
            else:
                self.x = self.z = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def yz(self) -> Vector2D:
        ''' Get the YZ components of the vector

        Returns:
            Vector2D
        '''

        return Vector2D(self.y, self.z)

    @yz.setter
    def yz(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 2)
                self.y = values[0]
                self.z = values[1]
            else:
                self.y = self.z = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def zx(self) -> Vector2D:
        ''' Get the ZX components of the vector

        Returns:
            Vector2D
        '''

        return Vector2D(self.z, self.x)

    @zx.setter
    def zx(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 2)
                self.z = values[0]
                self.x = values[1]
            else:
                self.z = self.x = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def zy(self) -> Vector2D:
        ''' Get the ZY components of the vector

        Returns:
            Vector2D
        '''

        return Vector2D(self.z, self.y)

    @zy.setter
    def zy(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 2)
                self.z = values[0]
                self.y = values[1]
            else:
                self.z = self.y = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def zz(self) -> Vector2D:
        ''' Get the ZZ components of the vector

        Returns:
            Vector2D
        '''

        return Vector2D.broadcast(self.z)

    @property
    def xxx(self) -> 'Vector3D':
        ''' Get the XXX components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D.broadcast(self.x)

    @property
    def xxy(self) -> 'Vector3D':
        ''' Get the XXY components of the vector

        Returns:
            Vector3D

        '''

        return Vector3D(self.x, self.x, self.y)

    @property
    def xxz(self) -> 'Vector3D':
        ''' Get the XXZ components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.x, self.x, self.z)

    @property
    def xyx(self) -> 'Vector3D':
        ''' Get the XYX components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.x, self.y, self.x)

    @property
    def xyy(self) -> 'Vector3D':
        ''' Get the XYY components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.x, self.y, self.y)

    @property
    def xyz(self) -> 'Vector3D':
        ''' Get the XYZ components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.x, self.y, self.z)

    @xyz.setter
    def xyz(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 3)
                self.x = values[0]
                self.y = values[1]
                self.z = values[2]
            else:
                self.z = self.y = self.z = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def xzx(self) -> 'Vector3D':
        ''' Get the XZX components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.x, self.z, self.x)

    @property
    def xzy(self) -> 'Vector3D':
        ''' Get the XZY components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.x, self.z, self.y)

    @xzy.setter
    def xzy(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 3)
                self.x = values[0]
                self.z = values[1]
                self.y = values[2]
            else:
                self.x = self.z = self.y = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def xzz(self) -> 'Vector3D':
        ''' Get the XZZ components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.x, self.z, self.z)

    @property
    def yxx(self) -> 'Vector3D':
        ''' Get the YXX components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.y, self.x, self.x)

    @property
    def yxy(self) -> 'Vector3D':
        ''' Get the YXY components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.y, self.x, self.y)

    @property
    def yxz(self) -> 'Vector3D':
        ''' Get the YXZ components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.y, self.x, self.z)

    @yxz.setter
    def yxz(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 3)
                self.y = values[0]
                self.x = values[1]
                self.z = values[2]
            else:
                self.y = self.x = self.z = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def yyx(self) -> 'Vector3D':
        ''' Get the YYX components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.y, self.y, self.x)

    @property
    def yyy(self) -> 'Vector3D':
        ''' Get the YYY components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D.broadcast(self.y)

    @property
    def yyz(self) -> 'Vector3D':
        ''' Get the YYZ components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.y, self.y, self.z)

    @property
    def yzx(self) -> 'Vector3D':
        ''' Get the YZX components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.y, self.z, self.x)

    @yzx.setter
    def yzx(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 3)
                self.y = values[0]
                self.z = values[1]
                self.x = values[2]
            else:
                self.y = self.z = self.x = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def yzy(self) -> 'Vector3D':
        ''' Get the YZY components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.y, self.z, self.y)

    @property
    def yzz(self) -> 'Vector3D':
        ''' Get the YZZ components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.y, self.z, self.z)

    @property
    def zxx(self) -> 'Vector3D':
        ''' Get the ZXX components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.z, self.x, self.x)

    @property
    def zxy(self) -> 'Vector3D':
        ''' Get the ZXY components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.z, self.x, self.y)

    @zxy.setter
    def zxy(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 3)
                self.z = values[0]
                self.x = values[1]
                self.y = values[2]
            else:
                self.z = self.x = self.y = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def zxz(self) -> 'Vector3D':
        ''' Get the ZXZ components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.z, self.x, self.z)

    @property
    def zyx(self) -> 'Vector3D':
        ''' Get the ZYX components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.z, self.y, self.x)

    @zyx.setter
    def zyx(self, value: Union[NUM, Iterable[NUM]]):
        try:
            if hasattr(value, '__iter__'):
                values = self._iter_conv_set(value, 3)
                self.z = values[0]
                self.y = values[1]
                self.x = values[2]
            else:
                self.z = self.y = self.x = float(value)
            if self.wrapped:
                raise VectorException(ERROR_SET_PROPERTY)
        except ValueError:
            raise VectorException(ERROR_SET_MESSAGE)

    @property
    def zyy(self) -> 'Vector3D':
        ''' Get the ZYY components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.z, self.y, self.y)

    @property
    def zyz(self) -> 'Vector3D':
        ''' Get the ZYZ components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.z, self.y, self.z)

    @property
    def zzx(self) -> 'Vector3D':
        ''' Get the ZZX components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.z, self.z, self.x)

    @property
    def zzy(self) -> 'Vector3D':
        ''' Get the ZZY components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D(self.z, self.z, self.y)

    @property
    def zzz(self) -> 'Vector3D':
        ''' Get the ZZZ components of the vector

        Returns:
            Vector3D
        '''

        return Vector3D.broadcast(self.z)

    def __add__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector3D':
        return Vector3D.from_tuple(np.add(self, other))

    def __radd__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector3D':
        return Vector3D.from_tuple(np.add(other, self))

    def __sub__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector3D':
        return Vector3D.from_tuple(np.subtract(self, other))

    def __rsub__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector3D':
        return Vector3D.from_tuple(np.subtract(other, self))

    def __mul__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector3D':
        return Vector3D.from_tuple(np.multiply(self, other))

    def __rmul__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector3D':
        return Vector3D.from_tuple(np.multiply(other, self))

    def __truediv__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector3D':
        return Vector3D.from_tuple(np.divide(self, other))

    def __rtruediv__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector3D':
        return Vector3D.from_tuple(np.divide(other, self))

    def __floordiv__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector3D':
        return Vector3D.from_tuple(np.floor_divide(self, other))

    def __rfloordiv__(self, other: Union[NUM, Iterable[NUM]]) -> 'Vector3D':
        return Vector3D.from_tuple(np.floor_divide(other, self))
