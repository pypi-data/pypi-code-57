'''_988.py

RootTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ROOT_TYPES = python_net_import('SMT.MastaAPI.DetailedRigidConnectors.Splines', 'RootTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('RootTypes',)


class RootTypes(Enum):
    '''RootTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _ROOT_TYPES

    __hash__ = None

    FLAT_ROOT = 0
    FILLET_ROOT = 1
