'''_719.py

CylindricalManufacturedVirtualGearInMesh
'''


from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _743
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_MANUFACTURED_VIRTUAL_GEAR_IN_MESH = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation', 'CylindricalManufacturedVirtualGearInMesh')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalManufacturedVirtualGearInMesh',)


class CylindricalManufacturedVirtualGearInMesh(_1.APIBase):
    '''CylindricalManufacturedVirtualGearInMesh

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_MANUFACTURED_VIRTUAL_GEAR_IN_MESH
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalManufacturedVirtualGearInMesh.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def load_direction_angle_for_iso_rating(self) -> 'float':
        '''float: 'LoadDirectionAngleForISORating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadDirectionAngleForISORating

    @property
    def bending_moment_arm_for_iso_rating(self) -> 'float':
        '''float: 'BendingMomentArmForISORating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BendingMomentArmForISORating

    @property
    def form_factor_for_iso_rating(self) -> 'float':
        '''float: 'FormFactorForISORating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FormFactorForISORating

    @property
    def stress_correction_factor_for_iso_rating(self) -> 'float':
        '''float: 'StressCorrectionFactorForISORating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StressCorrectionFactorForISORating

    @property
    def load_direction_for_agma_rating(self) -> 'float':
        '''float: 'LoadDirectionForAGMARating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LoadDirectionForAGMARating

    @property
    def tooth_root_chord_for_agma_rating(self) -> 'float':
        '''float: 'ToothRootChordForAGMARating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothRootChordForAGMARating

    @property
    def bending_moment_arm_for_agma_rating(self) -> 'float':
        '''float: 'BendingMomentArmForAGMARating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.BendingMomentArmForAGMARating

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def virtual_gear(self) -> '_743.VirtualSimulationCalculator':
        '''VirtualSimulationCalculator: 'VirtualGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_743.VirtualSimulationCalculator)(self.wrapped.VirtualGear) if self.wrapped.VirtualGear else None
