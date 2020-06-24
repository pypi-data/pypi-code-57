'''_2090.py

WormGear
'''


from mastapy.gears.gear_designs.worm import _722
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import _2069
from mastapy._internal.python_net import python_net_import

_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGear',)


class WormGear(_2069.Gear):
    '''WormGear

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGear.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def active_gear_design(self) -> '_722.WormGearDesign':
        '''WormGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_722.WormGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def worm_gear_design(self) -> '_722.WormGearDesign':
        '''WormGearDesign: 'WormGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_722.WormGearDesign)(self.wrapped.WormGearDesign) if self.wrapped.WormGearDesign else None
