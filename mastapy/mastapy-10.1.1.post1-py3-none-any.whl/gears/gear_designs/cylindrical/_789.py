'''_789.py

CylindricalGearTableMGItemDetail
'''


from enum import Enum

from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TABLE_MG_ITEM_DETAIL = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'CylindricalGearTableMGItemDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearTableMGItemDetail',)


class CylindricalGearTableMGItemDetail(Enum):
    '''CylindricalGearTableMGItemDetail

    This is a mastapy class.

    Note:
        This class is an Enum.
    '''

    @classmethod
    def type_(cls):
        return _CYLINDRICAL_GEAR_TABLE_MG_ITEM_DETAIL

    __hash__ = None

    CHART = 0
    REPORT = 1
    REPORT_AND_CHART = 2
