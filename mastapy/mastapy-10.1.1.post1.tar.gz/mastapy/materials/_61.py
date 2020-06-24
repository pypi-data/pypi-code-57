'''_61.py

FatigueSafetyFactorItemForPlastic
'''


from mastapy.materials import _60
from mastapy._internal.python_net import python_net_import

_FATIGUE_SAFETY_FACTOR_ITEM_FOR_PLASTIC = python_net_import('SMT.MastaAPI.Materials', 'FatigueSafetyFactorItemForPlastic')


__docformat__ = 'restructuredtext en'
__all__ = ('FatigueSafetyFactorItemForPlastic',)


class FatigueSafetyFactorItemForPlastic(_60.FatigueSafetyFactorItemBase):
    '''FatigueSafetyFactorItemForPlastic

    This is a mastapy class.
    '''

    TYPE = _FATIGUE_SAFETY_FACTOR_ITEM_FOR_PLASTIC

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FatigueSafetyFactorItemForPlastic.TYPE'):
        super().__init__(instance_to_wrap)
