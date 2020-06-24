'''conversion.py

This module is for converting between Pythonnet representations and mastapy
representations. Should only be used internally.
'''


from typing import List, TypeVar, Union, Sequence
from datetime import datetime
from io import BytesIO
from collections import OrderedDict
from numpy import ndarray

import clr
from PIL import Image

from mastapy._internal.python_net import python_net_import
from mastapy._internal.vector_3d import Vector3D
from mastapy._internal.tuple_with_name import TupleWithName
from mastapy._internal.implicit import enum_with_selected_value

_SYSTEM = python_net_import('System')
_IO = python_net_import('System.IO')
_IMAGE = python_net_import('System.Drawing.Image')
_LIST = python_net_import('System.Collections.Generic', 'List')
_VECTOR3D = python_net_import('SMT.MastaAPI.MathUtility', 'Vector3D')


class ConversionException(Exception):
    pass


# -----------------------------------------------------------------------
# - Object conversions
# -----------------------------------------------------------------------


def pn_to_mp_objects_in_iterable(iterable_of_objects, wrapper):
    '''Wraps up all Pythonnet objects returned in an iterable in mastapy types

    Args:
        iterable_of_objects: Iterable of Pythonnet objects
        wrapper: the wrapping mastapy type

    Returns:
        Iterable[wrapper]
    '''

    return (wrapper(x) for x in iterable_of_objects)


def pn_to_mp_objects_in_list(list_of_objects, wrapper):
    '''Wraps up all Pythonnet objects returned in a list in mastapy types

    Args:
        list_of_objects: List of Pythonnet objects
        wrapper: the wrapping mastapy type

    Returns:
        List[wrapper]
    '''

    return [wrapper(x) for x in list_of_objects]


def mp_to_pn_objects_in_list(list_of_objects):
    '''Unwraps all mastapy objects to a list of pythonnet objects

    Args:
        list_of_objects: List of mastapy objects

    Returns:
        List[x._TYPE]
    '''

    return [x.wrapped for x in list_of_objects]


def pn_to_mp_complex(pn_complex):
    '''Converts Masta API complex types to Python complex types

    Args:
        pn_complex: Masta API complex object

    Returns:
        complex
    '''

    return complex(pn_complex.Real, pn_complex.Imaginary)


def pn_to_mp_complex_list(pn_complex_list):
    '''Converts Masta API complex types in a list to Python complex types
    in a list

    Args:
        pn_complex: List of Masta API complex objects

    Returns:
        List[complex]
    '''

    return [pn_to_mp_complex(x) for x in pn_complex_list]


def pn_to_mp_enum(pn_enum):
    '''Converts C# enum to int

    Args:
        pn_enum: C# enum

    Returns:
        int
    '''
    return int(pn_enum)


def mp_to_pn_enum(mp_enum):
    '''Converts Python enum to C# enum

    Args:
        mp_enum: Python enum

    Returns:
        int
    '''
    return mp_enum.value if mp_enum else 0


def pn_to_mp_vector3d(pn_vector3d) -> Vector3D:
    '''Converts C# Vector3D and friends to a tuple

    Args:
        pn_vector3d: C# Vector3D (or similar)

    Returns:
        Vector3D
    '''

    return Vector3D.wrap(pn_vector3d)


def mp_to_pn_vector3d(mp_vector3d):
    '''Converts Python tuple to C# Vector3D

    Args:
        mp_vector3d: tuple

    Returns:
        C# Vector3D
    '''

    if (not hasattr(mp_vector3d, '__iter__')
            or len(mp_vector3d) != 3):
        raise ConversionException((
            'Failed to convert object to a Vector3D. '
            'Make sure that the object is iterable and contains exactly 3 '
            'components.'))

    return _VECTOR3D(mp_vector3d[0], mp_vector3d[1], mp_vector3d[2])


def pn_to_mp_tuple_with_name(pn_tuple_with_name, conversion_methods=None):
    '''Converts C# NamedTuple to Python TupleWithName

    Args:
        pn_tuple_with_name: C# NamedTuple
        conversion_methods (optional): conversion methods for items in tuple

    Returns:
        TupleWithName
    '''

    attrs = filter(None, map(
        lambda x: getattr(
            pn_tuple_with_name, 'Item' + str(x), None), range(1, 8)))
    converted = (
        map(
            lambda x: x[1](x[0]) if x[1] else x[0],
            zip(attrs, conversion_methods))
        if conversion_methods
        else attrs)
    return TupleWithName(*tuple(converted), name=pn_tuple_with_name.Name)


def pn_to_mp_datetime(pn_datetime):
    '''Converts C# System.DateTime struct to python datetime object

    Args:
        pn_datetime: C# System.DateTime struct

    Returns:
        datetime
    '''

    if not pn_datetime:
        return datetime.max

    year = pn_datetime.Year
    month = pn_datetime.Month
    day = pn_datetime.Day
    hour = pn_datetime.Hour
    minute = pn_datetime.Minute
    second = pn_datetime.Second
    microsecond = pn_datetime.Millisecond * 1000

    return datetime(year, month, day, hour, minute, second, microsecond)


def pn_to_mp_image(pn_image):
    '''Converts C# System.Drawing.Image to a PIL image

    Args:
        pn_image: C# System.Drawing.Image

    Returns:
        PIL.Image
    '''

    if not pn_image:
        return None

    image_format = python_net_import('System.Drawing.Imaging.ImageFormat')

    memory_stream = _IO.MemoryStream()
    pn_image.Save(memory_stream, image_format.Png)

    byte_data = bytes(memory_stream.ToArray())
    byte_stream = BytesIO(byte_data)
    image = Image.open(byte_stream)

    memory_stream.Dispose()

    return image


def mp_to_pn_image(mp_image):
    '''Converts PIL image to a C# System.Drawing.Image

    Args:
        mp_image: PIL image

    Returns:
        C# System.Drawing.Image
    '''

    if not mp_image:
        return None

    byte_stream = BytesIO()
    mp_image.save(byte_stream, format=mp_image.format)
    byte_data = byte_stream.getvalue()

    memory_stream = _IO.MemoryStream(byte_data)
    return _IMAGE.FromStream(memory_stream)


# -----------------------------------------------------------------------
# - Dictionary conversions
# -----------------------------------------------------------------------


def pn_to_mp_objects_in_list_in_ordered_dict(dict_of_objects, wrapper):
    '''Wraps up all Pythonnet objects returned in a list in a dictionary in
    mastapy types and returns Python list and OrderedDict structures

    Note:
        We assume that the key is a basic Python type.

    Args:
        dict_of_objects: Dictionary of lists of objects.
            e.g. {float : [PYTHON_NET_OBJECT, ...], ...}
        wrapper: the wrapping mastapy type

    Returns:
        OrderedDict[TKey, List[wrapper]]
    '''

    return OrderedDict(
        (kv.Key, [wrapper(obj) for obj in kv.Value])
        for kv in dict_of_objects)


def pn_to_mp_objects_in_list_in_dict(dict_of_objects, wrapper):
    '''Wraps up all Pythonnet objects returned in a list in a dictionary in
    mastapy types and returns Python list and dictionary structures

    Note:
        We assume that the key is a basic Python type.

    Args:
        dict_of_objects: Dictionary of lists of objects.
            e.g. {float: [PYTHON_NET_OBJECT, ...], ...}
        wrapper: the wrapping mastapy type

    Returns:
        Dict[TKey, List[wrapper]]
    '''

    return {
        kv.Key: [wrapper(obj) for obj in kv.Value]
        for kv in dict_of_objects}


# -----------------------------------------------------------------------
# - List conversions
# -----------------------------------------------------------------------


def pn_to_mp_bytes(pn_list: _SYSTEM.Array[_SYSTEM.Byte]) -> bytes:
    '''Converts a C# byte array to a bytes object

    Args:
        pn_list (System.Array[System.Byte]): 1D Array of bytes

    Returns:
        bytes
    '''

    return bytes([int(x) for x in pn_list])


def pn_to_mp_list_float(pn_list: _SYSTEM.Array[_SYSTEM.Double]) -> List[float]:
    '''Converts a 1D Array of Doubles to a list of floats

    Args:
        pn_list (System.Array[System.Double]): 1D Array

    Returns:
        List[float]
    '''

    return list(pn_list)


def mp_to_pn_array_float(
        mp_list: Union[
            ndarray, Sequence[float]]) -> _SYSTEM.Array[_SYSTEM.Double]:
    '''Converts a list of floats to a 1D array

    Args:
        mp_list (List[float]): List of floats

    Returns:
        System.Array[System.Double]: i.e. System.Double[]
    '''

    if mp_list is None or not any(mp_list):
        return _SYSTEM.Array.CreateInstance(_SYSTEM.Double, 0)

    if isinstance(mp_list, ndarray):
        if len(mp_list.shape) > 1:
            raise ConversionException((
                'Invalid argument provided. Argument must be a 1D array of '
                'float values.'))

    pn_list = _SYSTEM.Array.CreateInstance(_SYSTEM.Double, len(mp_list))
    for i, x in enumerate(mp_list):
        pn_list.SetValue(_SYSTEM.Double(x), i)
    return pn_list


def mp_to_pn_list_float(
        mp_list: Union[ndarray, Sequence[float]]) -> _LIST[_SYSTEM.Double]:
    '''Converts a list of floats to a 1D list

    Args:
        mp_list (List[float]): List of floats

    Returns:
        System.Collections.Generic.List[System.Double]
    '''

    if isinstance(mp_list, ndarray):
        if len(mp_list.shape) > 1:
            raise ConversionException((
                'Invalid argument provided. Argument must be a 1D array of '
                'float values.'))

    new_list = _LIST[_SYSTEM.Double]()
    for x in mp_list:
        new_list.Add(x)
    return new_list


def pn_to_mp_list_float_2d(
        pn_list: _SYSTEM.Array[_SYSTEM.Double]) -> List[List[float]]:
    '''Converts a 2D Array of Doubles to a list of lists of floats

    Args:
        pn_list (System.Array[System.Double]): 2D Array

    Returns:
        List[List[float]]
    '''

    side_length = pn_list.GetLength(0)
    return [
        [pn_list.Get(y, x) for x in range(side_length)]
        for y in range(side_length)]


def mp_to_pn_list_float_2d(
        mp_list: List[List[float]]) -> _SYSTEM.Array[_SYSTEM.Double]:
    '''Converts a list of lists of floats to a 2D array

    Args:
        mp_list (List[List[float]]): List of lists of floats

    Returns:
        System.Array[System.Double]: i.e. System.Double[,]
    '''

    if mp_list is None or not any(mp_list):
        return _SYSTEM.Array.CreateInstance(_SYSTEM.Double, 0, 0)

    side_length = len(mp_list)
    pn_list = _SYSTEM.Array.CreateInstance(
        _SYSTEM.Double, side_length, side_length)
    for i, y in enumerate(mp_list):
        if len(y) != side_length:
            raise ConversionException((
                'Invalid argument provided. Argument must be a '
                'square matrix (i.e. [[1.0, 0.0], [0.0, 1.0]])'))
        for j, x in enumerate(y):
            pn_list.SetValue(float(x), i, j)
    return pn_list
