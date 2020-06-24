'''_3076.py

RootAssemblyCompoundPowerFlow
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.load_case_groups import (
    _2066, _1970, _1968, _4922
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.power_flows.compound import _3150
from mastapy._internal.python_net import python_net_import

_ROOT_ASSEMBLY_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'RootAssemblyCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RootAssemblyCompoundPowerFlow',)


class RootAssemblyCompoundPowerFlow(_3150.AssemblyCompoundPowerFlow):
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
    def compound_static_load(self) -> '_2066.AbstractStaticLoadCaseGroup':
        '''AbstractStaticLoadCaseGroup: 'CompoundStaticLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2066.AbstractStaticLoadCaseGroup)(self.wrapped.CompoundStaticLoad) if self.wrapped.CompoundStaticLoad else None

    @property
    def compound_static_load_of_type_duty_cycle(self) -> '_1970.DutyCycle':
        '''DutyCycle: 'CompoundStaticLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CompoundStaticLoad.__class__.__qualname__ != 'DutyCycle':
            raise CastException('Failed to cast compound_static_load to DutyCycle. Expected: {}.'.format(self.wrapped.CompoundStaticLoad.__class__.__qualname__))

        return constructor.new(_1970.DutyCycle)(self.wrapped.CompoundStaticLoad) if self.wrapped.CompoundStaticLoad else None

    @property
    def compound_static_load_of_type_design_state(self) -> '_1968.DesignState':
        '''DesignState: 'CompoundStaticLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CompoundStaticLoad.__class__.__qualname__ != 'DesignState':
            raise CastException('Failed to cast compound_static_load to DesignState. Expected: {}.'.format(self.wrapped.CompoundStaticLoad.__class__.__qualname__))

        return constructor.new(_1968.DesignState)(self.wrapped.CompoundStaticLoad) if self.wrapped.CompoundStaticLoad else None

    @property
    def compound_static_load_of_type_sub_group_in_single_design_state(self) -> '_4922.SubGroupInSingleDesignState':
        '''SubGroupInSingleDesignState: 'CompoundStaticLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.CompoundStaticLoad.__class__.__qualname__ != 'SubGroupInSingleDesignState':
            raise CastException('Failed to cast compound_static_load to SubGroupInSingleDesignState. Expected: {}.'.format(self.wrapped.CompoundStaticLoad.__class__.__qualname__))

        return constructor.new(_4922.SubGroupInSingleDesignState)(self.wrapped.CompoundStaticLoad) if self.wrapped.CompoundStaticLoad else None
