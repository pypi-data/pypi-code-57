'''_77.py

BarModelExportType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_BAR_MODEL_EXPORT_TYPE = python_net_import('SMT.MastaAPI.NodalAnalysis', 'BarModelExportType')


__docformat__ = 'restructuredtext en'
__all__ = ('BarModelExportType',)


class BarModelExportType(Enum):
    '''BarModelExportType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _BAR_MODEL_EXPORT_TYPE
    __hash__ = None

    BAR_ELEMENTS = 0
    MATRIX_ELEMENTS = 1
    SOLID_SHAFTS = 2
