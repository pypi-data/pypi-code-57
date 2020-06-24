'''_6137.py

ImportType
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_IMPORT_TYPE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ImportType')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportType',)


class ImportType(Enum):
    '''ImportType

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _IMPORT_TYPE

    __hash__ = None

    DUTY_CYCLE_TIME_SERIES = 0
    INDIVIDUAL_LOAD_CASE = 1
    INDIVIDUAL_LOAD_CASES_AS_TIME_SERIES = 2
