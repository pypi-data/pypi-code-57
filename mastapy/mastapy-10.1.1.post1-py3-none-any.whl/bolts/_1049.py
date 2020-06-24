'''_1049.py

JointGeometries
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_JOINT_GEOMETRIES = python_net_import('SMT.MastaAPI.Bolts', 'JointGeometries')


__docformat__ = 'restructuredtext en'
__all__ = ('JointGeometries',)


class JointGeometries(Enum):
    '''JointGeometries

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _JOINT_GEOMETRIES

    __hash__ = None

    PRISMATIC_BODY = 0
    BEAM = 1
    CIRCULAR_PLATE = 2
    FLANGE = 3
    SYMMETRIC_MULTI_BOLTED_JOINT = 4
    ASYMMETRIC_MULTI_BOLTED_JOINT = 5
