'''_2697.py

CylindricalGearSetCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1968
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _2696, _2764, _2700
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3714
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'CylindricalGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundDynamicAnalysis',)


class CylindricalGearSetCompoundDynamicAnalysis(_2700.GearSetCompoundDynamicAnalysis):
    '''CylindricalGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def cylindrical_gears_compound_dynamic_analysis(self) -> 'List[_2696.CylindricalGearCompoundDynamicAnalysis]':
        '''List[CylindricalGearCompoundDynamicAnalysis]: 'CylindricalGearsCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundDynamicAnalysis, constructor.new(_2696.CylindricalGearCompoundDynamicAnalysis))
        return value

    @property
    def cylindrical_meshes_compound_dynamic_analysis(self) -> 'List[_2764.CylindricalGearMeshCompoundDynamicAnalysis]':
        '''List[CylindricalGearMeshCompoundDynamicAnalysis]: 'CylindricalMeshesCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundDynamicAnalysis, constructor.new(_2764.CylindricalGearMeshCompoundDynamicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3714.CylindricalGearSetDynamicAnalysis]':
        '''List[CylindricalGearSetDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3714.CylindricalGearSetDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_3714.CylindricalGearSetDynamicAnalysis]':
        '''List[CylindricalGearSetDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_3714.CylindricalGearSetDynamicAnalysis))
        return value
