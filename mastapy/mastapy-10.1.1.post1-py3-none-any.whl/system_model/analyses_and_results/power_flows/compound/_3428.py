'''_3428.py

RootAssemblyCompoundPowerFlow
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.load_case_groups import (
    _5234, _5232, _5237, _5238,
    _5242
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.power_flows.compound import _3346
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'RootAssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundPowerFlow',)


class RootAssemblyCompoundPowerFlow(_3346.AssemblyCompoundPowerFlow):
    '''RootAssemblyCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _ROOT_ASSEMBLY_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RootAssemblyCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def set_face_widths_for_specified_safety_factors(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetFaceWidthsForSpecifiedSafetyFactors' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetFaceWidthsForSpecifiedSafetyFactors

    @property
    def compound_static_load(self) -> '_5234.AbstractStaticLoadCaseGroup':
        '''AbstractStaticLoadCaseGroup: 'CompoundStaticLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5234.AbstractStaticLoadCaseGroup)(self.wrapped.CompoundStaticLoad) if self.wrapped.CompoundStaticLoad else None

    @property
    def compound_static_load_of_type_abstract_design_state_load_case_group(self) -> '_5232.AbstractDesignStateLoadCaseGroup':
        '''AbstractDesignStateLoadCaseGroup: 'CompoundStaticLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5232.AbstractDesignStateLoadCaseGroup.TYPE not in self.wrapped.CompoundStaticLoad.__class__.__mro__:
            raise CastException('Failed to cast compound_static_load to AbstractDesignStateLoadCaseGroup. Expected: {}.'.format(self.wrapped.CompoundStaticLoad.__class__.__qualname__))

        return constructor.new(_5232.AbstractDesignStateLoadCaseGroup)(self.wrapped.CompoundStaticLoad) if self.wrapped.CompoundStaticLoad else None

    @property
    def compound_static_load_of_type_design_state(self) -> '_5237.DesignState':
        '''DesignState: 'CompoundStaticLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5237.DesignState.TYPE not in self.wrapped.CompoundStaticLoad.__class__.__mro__:
            raise CastException('Failed to cast compound_static_load to DesignState. Expected: {}.'.format(self.wrapped.CompoundStaticLoad.__class__.__qualname__))

        return constructor.new(_5237.DesignState)(self.wrapped.CompoundStaticLoad) if self.wrapped.CompoundStaticLoad else None

    @property
    def compound_static_load_of_type_duty_cycle(self) -> '_5238.DutyCycle':
        '''DutyCycle: 'CompoundStaticLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5238.DutyCycle.TYPE not in self.wrapped.CompoundStaticLoad.__class__.__mro__:
            raise CastException('Failed to cast compound_static_load to DutyCycle. Expected: {}.'.format(self.wrapped.CompoundStaticLoad.__class__.__qualname__))

        return constructor.new(_5238.DutyCycle)(self.wrapped.CompoundStaticLoad) if self.wrapped.CompoundStaticLoad else None

    @property
    def compound_static_load_of_type_sub_group_in_single_design_state(self) -> '_5242.SubGroupInSingleDesignState':
        '''SubGroupInSingleDesignState: 'CompoundStaticLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _5242.SubGroupInSingleDesignState.TYPE not in self.wrapped.CompoundStaticLoad.__class__.__mro__:
            raise CastException('Failed to cast compound_static_load to SubGroupInSingleDesignState. Expected: {}.'.format(self.wrapped.CompoundStaticLoad.__class__.__qualname__))

        return constructor.new(_5242.SubGroupInSingleDesignState)(self.wrapped.CompoundStaticLoad) if self.wrapped.CompoundStaticLoad else None
