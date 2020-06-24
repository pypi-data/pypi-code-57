'''_6173.py

SystemOptimiserTargets
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_SYSTEM_OPTIMISER_TARGETS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'SystemOptimiserTargets')


__docformat__ = 'restructuredtext en'
__all__ = ('SystemOptimiserTargets',)


class SystemOptimiserTargets(Enum):
    '''SystemOptimiserTargets

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _SYSTEM_OPTIMISER_TARGETS
    __hash__ = None

    MINIMUM_FACE_WIDTH = 0
    MINIMUM_MASS = 1
    MINIMUM_WIDEST_FACE_WIDTH = 2
    CONTACT_RATIO_FIXED_FACE_WIDTH = 3
