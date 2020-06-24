'''_93.py

FEStiffnessTester
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.nodal_analysis import _91
from mastapy.system_model.imported_fes import _101
from mastapy._internal.cast_exception import CastException
from mastapy.gears.ltca.cylindrical import _102, _104
from mastapy.gears.ltca.conical import _103, _105
from mastapy.math_utility.measured_vectors import _106
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_FE_STIFFNESS_TESTER = python_net_import('SMT.MastaAPI.NodalAnalysis', 'FEStiffnessTester')


__docformat__ = 'restructuredtext en'
__all__ = ('FEStiffnessTester',)


class FEStiffnessTester(_1.APIBase):
    '''FEStiffnessTester

    This is a mastapy class.
    '''

    TYPE = _FE_STIFFNESS_TESTER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEStiffnessTester.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def force_scaling_factor(self) -> 'float':
        '''float: 'ForceScalingFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceScalingFactor

    @property
    def displacement_scaling_factor(self) -> 'float':
        '''float: 'DisplacementScalingFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DisplacementScalingFactor

    @property
    def fe_stiffness(self) -> '_91.FEStiffness':
        '''FEStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_91.FEStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_imported_fe(self) -> '_101.ImportedFE':
        '''ImportedFE: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.FEStiffness.__class__.__qualname__ != 'ImportedFE':
            raise CastException('Failed to cast fe_stiffness to ImportedFE. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_101.ImportedFE)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_cylindrical_gear_bending_stiffness(self) -> '_102.CylindricalGearBendingStiffness':
        '''CylindricalGearBendingStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.FEStiffness.__class__.__qualname__ != 'CylindricalGearBendingStiffness':
            raise CastException('Failed to cast fe_stiffness to CylindricalGearBendingStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_102.CylindricalGearBendingStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_conical_gear_bending_stiffness(self) -> '_103.ConicalGearBendingStiffness':
        '''ConicalGearBendingStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.FEStiffness.__class__.__qualname__ != 'ConicalGearBendingStiffness':
            raise CastException('Failed to cast fe_stiffness to ConicalGearBendingStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_103.ConicalGearBendingStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_cylindrical_gear_contact_stiffness(self) -> '_104.CylindricalGearContactStiffness':
        '''CylindricalGearContactStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.FEStiffness.__class__.__qualname__ != 'CylindricalGearContactStiffness':
            raise CastException('Failed to cast fe_stiffness to CylindricalGearContactStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_104.CylindricalGearContactStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def fe_stiffness_of_type_conical_gear_contact_stiffness(self) -> '_105.ConicalGearContactStiffness':
        '''ConicalGearContactStiffness: 'FEStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.FEStiffness.__class__.__qualname__ != 'ConicalGearContactStiffness':
            raise CastException('Failed to cast fe_stiffness to ConicalGearContactStiffness. Expected: {}.'.format(self.wrapped.FEStiffness.__class__.__qualname__))

        return constructor.new(_105.ConicalGearContactStiffness)(self.wrapped.FEStiffness) if self.wrapped.FEStiffness else None

    @property
    def force_and_displacement_results(self) -> 'List[_106.ForceAndDisplacementResults]':
        '''List[ForceAndDisplacementResults]: 'ForceAndDisplacementResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ForceAndDisplacementResults, constructor.new(_106.ForceAndDisplacementResults))
        return value
