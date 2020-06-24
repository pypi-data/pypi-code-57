'''_1050.py

JointTypes
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_JOINT_TYPES = python_net_import('SMT.MastaAPI.Bolts', 'JointTypes')


__docformat__ = 'restructuredtext en'
__all__ = ('JointTypes',)


class JointTypes(Enum):
    '''JointTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _JOINT_TYPES

    __hash__ = None

    SV1 = 0
    SV2 = 1
    SV3 = 2
    SV4 = 3
    SV5 = 4
    SV6 = 5
