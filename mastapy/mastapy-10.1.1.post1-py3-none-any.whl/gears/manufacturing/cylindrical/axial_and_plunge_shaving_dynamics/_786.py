'''_786.py

ShavingDynamics
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs.cylindrical import _848
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_SHAVING_DYNAMICS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'ShavingDynamics')


__docformat__ = 'restructuredtext en'
__all__ = ('ShavingDynamics',)


class ShavingDynamics(_1.APIBase):
    '''ShavingDynamics

    This is a mastapy class.
    '''

    TYPE = _SHAVING_DYNAMICS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShavingDynamics.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def selected(self) -> 'bool':
        '''bool: 'Selected' is the original name of this property.'''

        return self.wrapped.Selected

    @selected.setter
    def selected(self, value: 'bool'):
        self.wrapped.Selected = bool(value) if value else False

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def crossed_axis_calculation_details(self) -> '_848.CrossedAxisCylindricalGearPairPointContact':
        '''CrossedAxisCylindricalGearPairPointContact: 'CrossedAxisCalculationDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_848.CrossedAxisCylindricalGearPairPointContact)(self.wrapped.CrossedAxisCalculationDetails) if self.wrapped.CrossedAxisCalculationDetails else None
