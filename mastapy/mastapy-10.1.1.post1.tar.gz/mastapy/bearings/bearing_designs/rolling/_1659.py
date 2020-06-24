'''_1659.py

ToroidalRollerBearing
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_designs.rolling import _1687
from mastapy._internal.python_net import python_net_import

_TOROIDAL_ROLLER_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'ToroidalRollerBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('ToroidalRollerBearing',)


class ToroidalRollerBearing(_1687.BarrelRollerBearing):
    '''ToroidalRollerBearing

    This is a mastapy class.
    '''

    TYPE = _TOROIDAL_ROLLER_BEARING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ToroidalRollerBearing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def operating_clearance_factor(self) -> 'float':
        '''float: 'OperatingClearanceFactor' is the original name of this property.'''

        return self.wrapped.OperatingClearanceFactor

    @operating_clearance_factor.setter
    def operating_clearance_factor(self, value: 'float'):
        self.wrapped.OperatingClearanceFactor = float(value) if value else 0.0

    @property
    def axial_displacement_guideline_value_s1(self) -> 'float':
        '''float: 'AxialDisplacementGuidelineValueS1' is the original name of this property.'''

        return self.wrapped.AxialDisplacementGuidelineValueS1

    @axial_displacement_guideline_value_s1.setter
    def axial_displacement_guideline_value_s1(self, value: 'float'):
        self.wrapped.AxialDisplacementGuidelineValueS1 = float(value) if value else 0.0

    @property
    def axial_displacement_guideline_value_s2(self) -> 'float':
        '''float: 'AxialDisplacementGuidelineValueS2' is the original name of this property.'''

        return self.wrapped.AxialDisplacementGuidelineValueS2

    @axial_displacement_guideline_value_s2.setter
    def axial_displacement_guideline_value_s2(self, value: 'float'):
        self.wrapped.AxialDisplacementGuidelineValueS2 = float(value) if value else 0.0

    @property
    def left_axial_displacement_limit(self) -> 'float':
        '''float: 'LeftAxialDisplacementLimit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LeftAxialDisplacementLimit

    @property
    def right_axial_displacement_limit(self) -> 'float':
        '''float: 'RightAxialDisplacementLimit' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RightAxialDisplacementLimit
