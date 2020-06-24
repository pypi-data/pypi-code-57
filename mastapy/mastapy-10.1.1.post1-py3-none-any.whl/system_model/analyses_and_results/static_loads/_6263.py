'''_6263.py

ElectricMachineDataImportType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_ELECTRIC_MACHINE_DATA_IMPORT_TYPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ElectricMachineDataImportType')


__docformat__ = 'restructuredtext en'
__all__ = ('ElectricMachineDataImportType',)


class ElectricMachineDataImportType(Enum):
    '''ElectricMachineDataImportType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    TYPE = _ELECTRIC_MACHINE_DATA_IMPORT_TYPE
    __hash__ = None

    EXCEL = 0
    JMAG = 1
    MOTORCAD = 2
