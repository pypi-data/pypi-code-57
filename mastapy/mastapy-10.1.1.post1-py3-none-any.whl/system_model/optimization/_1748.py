'''_1748.py

MicroGeometryOptimisationTarget
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_MICRO_GEOMETRY_OPTIMISATION_TARGET = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'MicroGeometryOptimisationTarget')


__docformat__ = 'restructuredtext en'
__all__ = ('MicroGeometryOptimisationTarget',)


class MicroGeometryOptimisationTarget(Enum):
    '''MicroGeometryOptimisationTarget

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _MICRO_GEOMETRY_OPTIMISATION_TARGET
    __hash__ = None

    TRANSMISSION_ERROR = 0
    CONTACT_STRESS = 1
