'''_114.py

StressResultsType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_STRESS_RESULTS_TYPE = python_net_import('SMT.MastaAPI.NodalAnalysis', 'StressResultsType')


__docformat__ = 'restructuredtext en'
__all__ = ('StressResultsType',)


class StressResultsType(Enum):
    '''StressResultsType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _STRESS_RESULTS_TYPE
    __hash__ = None

    MAXIMUM_TENSILE_PRINCIPAL_STRESS = 0
    VON_MISES_STRESS = 1
    X_COMPONENT = 2
    Y_COMPONENT = 3
    Z_COMPONENT = 4
    XY_SHEAR_STRESS = 5
    YZ_SHEAR_STRESS = 6
    XZ_SHEAR_STRESS = 7
    _1ST_PRINCIPAL_STRESS = 8
    _2ND_PRINCIPAL_STRESS = 9
    _3RD_PRINCIPAL_STRESS = 10
    STRESS_INTENSITY = 11
