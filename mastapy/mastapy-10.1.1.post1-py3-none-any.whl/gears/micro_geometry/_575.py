'''_575.py

LocationOfRootReliefEvaluation
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_LOCATION_OF_ROOT_RELIEF_EVALUATION = python_net_import('SMT.MastaAPI.Gears.MicroGeometry', 'LocationOfRootReliefEvaluation')


__docformat__ = 'restructuredtext en'
__all__ = ('LocationOfRootReliefEvaluation',)


class LocationOfRootReliefEvaluation(Enum):
    '''LocationOfRootReliefEvaluation

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _LOCATION_OF_ROOT_RELIEF_EVALUATION
    __hash__ = None

    ROOT_FORM = 0
    LOWER_EVALUATION_LIMIT = 1
    USERSPECIFIED = 2
