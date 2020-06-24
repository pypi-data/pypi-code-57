'''_6352.py

UseVariableBearingStiffnessOptions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_USE_VARIABLE_BEARING_STIFFNESS_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'UseVariableBearingStiffnessOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('UseVariableBearingStiffnessOptions',)


class UseVariableBearingStiffnessOptions(Enum):
    '''UseVariableBearingStiffnessOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _USE_VARIABLE_BEARING_STIFFNESS_OPTIONS

    __hash__ = None

    YES = 0
    NO = 1
    SPECIFY_FOR_EACH_BEARING = 2
