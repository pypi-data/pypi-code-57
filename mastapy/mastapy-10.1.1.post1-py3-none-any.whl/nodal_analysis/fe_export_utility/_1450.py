'''_1450.py

FEExportFormat
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_FE_EXPORT_FORMAT = python_net_import('SMT.MastaAPI.NodalAnalysis.FeExportUtility', 'FEExportFormat')


__docformat__ = 'restructuredtext en'
__all__ = ('FEExportFormat',)


class FEExportFormat(Enum):
    '''FEExportFormat

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _FE_EXPORT_FORMAT

    __hash__ = None

    ANSYS_APDL_INPUT_FILE = 0
    ANSYS_WORKBENCH_COMMANDS = 1
    NASTRAN_BULK_DATA_FILE = 2
    ABAQUS_INPUT_FILE = 3
