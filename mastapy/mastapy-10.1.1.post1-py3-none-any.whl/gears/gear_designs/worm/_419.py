'''_419.py

WormGearDesign
'''


from mastapy._internal import constructor, conversion
from mastapy.gears import _310
from mastapy.gears.gear_designs import _663
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Worm', 'WormGearDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearDesign',)


class WormGearDesign(_663.GearDesign):
    '''WormGearDesign

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def whole_depth(self) -> 'float':
        '''float: 'WholeDepth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WholeDepth

    @property
    def root_diameter(self) -> 'float':
        '''float: 'RootDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RootDiameter

    @property
    def hand(self) -> '_310.Hand':
        '''Hand: 'Hand' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Hand)
        return constructor.new(_310.Hand)(value) if value else None

    @hand.setter
    def hand(self, value: '_310.Hand'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Hand = value
