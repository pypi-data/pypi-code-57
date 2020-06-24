'''_2039.py

GearSetConfiguration
'''


from typing import List, Optional

from mastapy.gears import _300, _301
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import (
    _1968, _1969, _1970, _1971
)
from mastapy.system_model.analyses_and_results.static_loads import _2057
from mastapy.gears.analysis import _1123
from mastapy.system_model.analyses_and_results.load_case_groups import _2065
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_GEAR_SET_CONFIGURATION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSetConfiguration')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetConfiguration',)


class GearSetConfiguration(_1.APIBase):
    '''GearSetConfiguration

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_CONFIGURATION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetConfiguration.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_set_design_group(self) -> '_300.GearSetDesignGroup':
        '''GearSetDesignGroup: 'GearSetDesignGroup' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_300.GearSetDesignGroup)(self.wrapped.GearSetDesignGroup) if self.wrapped.GearSetDesignGroup else None

    @property
    def cylindrical_gear_sets(self) -> 'List[_1968.CylindricalGearSet]':
        '''List[CylindricalGearSet]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_1968.CylindricalGearSet))
        return value

    @property
    def conical_gear_sets(self) -> 'List[_1969.ConicalGearSet]':
        '''List[ConicalGearSet]: 'ConicalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConicalGearSets, constructor.new(_1969.ConicalGearSet))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_1970.WormGearSet]':
        '''List[WormGearSet]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_1970.WormGearSet))
        return value

    @property
    def klingelnberg_cyclo_palloid_gear_sets(self) -> 'List[_1971.KlingelnbergCycloPalloidConicalGearSet]':
        '''List[KlingelnbergCycloPalloidConicalGearSet]: 'KlingelnbergCycloPalloidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidGearSets, constructor.new(_1971.KlingelnbergCycloPalloidConicalGearSet))
        return value

    def implementation_detail_results_for(self, analysis_case: '_2057.StaticLoadCase', gear_set_mode: '_301.GearSetModes', run_all_planetary_meshes: 'bool') -> '_1123.GearSetGroupDutyCycle':
        ''' 'ImplementationDetailResultsFor' is the original name of this method.

        Args:
            analysis_case (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
            gear_set_mode (mastapy.gears.GearSetModes)
            run_all_planetary_meshes (bool)

        Returns:
            mastapy.gears.analysis.GearSetGroupDutyCycle
        '''

        gear_set_mode = conversion.mp_to_pn_enum(gear_set_mode)
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        method_result = self.wrapped.ImplementationDetailResultsFor(analysis_case.wrapped if analysis_case else None, gear_set_mode, run_all_planetary_meshes if run_all_planetary_meshes else False)
        return constructor.new(_1123.GearSetGroupDutyCycle)(method_result) if method_result else None

    def implementation_detail_results_for_group(self, analysis_case: '_2065.AbstractStaticLoadCaseGroup', gear_set_mode: '_301.GearSetModes', run_all_planetary_meshes: 'bool') -> '_1123.GearSetGroupDutyCycle':
        ''' 'ImplementationDetailResultsFor' is the original name of this method.

        Args:
            analysis_case (mastapy.system_model.analyses_and_results.load_case_groups.AbstractStaticLoadCaseGroup)
            gear_set_mode (mastapy.gears.GearSetModes)
            run_all_planetary_meshes (bool)

        Returns:
            mastapy.gears.analysis.GearSetGroupDutyCycle
        '''

        gear_set_mode = conversion.mp_to_pn_enum(gear_set_mode)
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        method_result = self.wrapped.ImplementationDetailResultsFor(analysis_case.wrapped if analysis_case else None, gear_set_mode, run_all_planetary_meshes if run_all_planetary_meshes else False)
        return constructor.new(_1123.GearSetGroupDutyCycle)(method_result) if method_result else None

    def perform_implementation_detail_analysis(self, static_load: '_2057.StaticLoadCase', gear_set_mode: '_301.GearSetModes', run_all_planetary_meshes: Optional['bool'] = True, perform_system_analysis_if_not_ready: Optional['bool'] = True):
        ''' 'PerformImplementationDetailAnalysis' is the original name of this method.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
            gear_set_mode (mastapy.gears.GearSetModes)
            run_all_planetary_meshes (bool, optional)
            perform_system_analysis_if_not_ready (bool, optional)
        '''

        gear_set_mode = conversion.mp_to_pn_enum(gear_set_mode)
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        perform_system_analysis_if_not_ready = bool(perform_system_analysis_if_not_ready)
        self.wrapped.PerformImplementationDetailAnalysis(static_load.wrapped if static_load else None, gear_set_mode, run_all_planetary_meshes if run_all_planetary_meshes else False, perform_system_analysis_if_not_ready if perform_system_analysis_if_not_ready else False)

    def perform_implementation_detail_analysis_group(self, static_load_case_group: '_2065.AbstractStaticLoadCaseGroup', gear_set_mode: '_301.GearSetModes', run_all_planetary_meshes: Optional['bool'] = True, perform_system_analysis_if_not_ready: Optional['bool'] = True):
        ''' 'PerformImplementationDetailAnalysis' is the original name of this method.

        Args:
            static_load_case_group (mastapy.system_model.analyses_and_results.load_case_groups.AbstractStaticLoadCaseGroup)
            gear_set_mode (mastapy.gears.GearSetModes)
            run_all_planetary_meshes (bool, optional)
            perform_system_analysis_if_not_ready (bool, optional)
        '''

        gear_set_mode = conversion.mp_to_pn_enum(gear_set_mode)
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        perform_system_analysis_if_not_ready = bool(perform_system_analysis_if_not_ready)
        self.wrapped.PerformImplementationDetailAnalysis(static_load_case_group.wrapped if static_load_case_group else None, gear_set_mode, run_all_planetary_meshes if run_all_planetary_meshes else False, perform_system_analysis_if_not_ready if perform_system_analysis_if_not_ready else False)
