'''_240.py

CompositeFatigueSafetyFactorItemForPlastic
'''


from mastapy.materials import _246
from mastapy._internal.python_net import python_net_import

_COMPOSITE_FATIGUE_SAFETY_FACTOR_ITEM_FOR_PLASTIC = python_net_import('SMT.MastaAPI.Materials', 'CompositeFatigueSafetyFactorItemForPlastic')


__docformat__ = 'restructuredtext en'
__all__ = ('CompositeFatigueSafetyFactorItemForPlastic',)


class CompositeFatigueSafetyFactorItemForPlastic(_246.FatigueSafetyFactorItemForPlastic):
    '''CompositeFatigueSafetyFactorItemForPlastic

    This is a mastapy class.
    '''

    TYPE = _COMPOSITE_FATIGUE_SAFETY_FACTOR_ITEM_FOR_PLASTIC
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompositeFatigueSafetyFactorItemForPlastic.TYPE'):
        super().__init__(instance_to_wrap)
