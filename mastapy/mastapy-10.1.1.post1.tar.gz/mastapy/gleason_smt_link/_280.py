'''_280.py

CutterMethod
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CUTTER_METHOD = python_net_import('SMT.MastaAPI.GleasonSMTLink', 'CutterMethod')


__docformat__ = 'restructuredtext en'
__all__ = ('CutterMethod',)


class CutterMethod(Enum):
    '''CutterMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _CUTTER_METHOD
    __hash__ = None

    FACE_MILLING = 1
    FACE_HOBBING = 9
