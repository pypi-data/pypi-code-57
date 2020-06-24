'''_1133.py

FitTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FIT_TYPES = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'FitTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('FitTypes',)


class FitTypes(Enum):
    '''FitTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _FIT_TYPES
    __hash__ = None

    SIDE_FIT = 0
    MAJOR_DIAMETER_FIT = 1
