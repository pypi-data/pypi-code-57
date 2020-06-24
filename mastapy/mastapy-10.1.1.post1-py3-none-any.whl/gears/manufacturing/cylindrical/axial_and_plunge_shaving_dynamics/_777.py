'''_777.py

PlungeShaverDynamicSettings
'''


from mastapy._internal import constructor, conversion
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_DYNAMIC_SETTINGS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'PlungeShaverDynamicSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverDynamicSettings',)


class PlungeShaverDynamicSettings(_1.APIBase):
    '''PlungeShaverDynamicSettings

    This is a mastapy class.
    '''

    TYPE = _PLUNGE_SHAVER_DYNAMIC_SETTINGS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlungeShaverDynamicSettings.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def calculation_accuracy(self) -> 'PlungeShaverDynamicSettings.PlungeShavingDynamicAccuracy':
        '''PlungeShavingDynamicAccuracy: 'CalculationAccuracy' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CalculationAccuracy)
        return constructor.new(PlungeShaverDynamicSettings.PlungeShavingDynamicAccuracy)(value) if value else None

    @calculation_accuracy.setter
    def calculation_accuracy(self, value: 'PlungeShaverDynamicSettings.PlungeShavingDynamicAccuracy'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CalculationAccuracy = value

    @property
    def calculation_flank(self) -> 'PlungeShaverDynamicSettings.PlungeShavingDynamicFlank':
        '''PlungeShavingDynamicFlank: 'CalculationFlank' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CalculationFlank)
        return constructor.new(PlungeShaverDynamicSettings.PlungeShavingDynamicFlank)(value) if value else None

    @calculation_flank.setter
    def calculation_flank(self, value: 'PlungeShaverDynamicSettings.PlungeShavingDynamicFlank'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CalculationFlank = value

    @property
    def section_locations(self) -> 'PlungeShaverDynamicSettings.PlungeShavingDynamicsSection':
        '''PlungeShavingDynamicsSection: 'SectionLocations' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.SectionLocations)
        return constructor.new(PlungeShaverDynamicSettings.PlungeShavingDynamicsSection)(value) if value else None

    @section_locations.setter
    def section_locations(self, value: 'PlungeShaverDynamicSettings.PlungeShavingDynamicsSection'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.SectionLocations = value
