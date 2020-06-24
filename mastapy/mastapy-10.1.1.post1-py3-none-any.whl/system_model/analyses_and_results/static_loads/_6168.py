'''_6168.py

ResetMicroGeometryOptions
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_RESET_MICRO_GEOMETRY_OPTIONS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'ResetMicroGeometryOptions')


__docformat__ = 'restructuredtext en'
__all__ = ('ResetMicroGeometryOptions',)


class ResetMicroGeometryOptions(Enum):
    '''ResetMicroGeometryOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _RESET_MICRO_GEOMETRY_OPTIONS

    __hash__ = None

    BLANK = 0
    RESET_TO_DESIGN_MICRO_GEOMETRY = 1
    RESET_TO_NO_MODIFICATION = 2
    COPY_TO_NEW_DESIGN_MICRO_GEOMETRY = 3
