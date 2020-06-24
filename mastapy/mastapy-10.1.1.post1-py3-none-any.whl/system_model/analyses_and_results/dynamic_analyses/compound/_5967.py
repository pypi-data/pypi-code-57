'''_5967.py

FaceGearSetCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2068
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _5965, _5966, _5971
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5846
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'FaceGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundDynamicAnalysis',)


class FaceGearSetCompoundDynamicAnalysis(_5971.GearSetCompoundDynamicAnalysis):
    '''FaceGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2068.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2068.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2068.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2068.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_dynamic_analysis(self) -> 'List[_5965.FaceGearCompoundDynamicAnalysis]':
        '''List[FaceGearCompoundDynamicAnalysis]: 'FaceGearsCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundDynamicAnalysis, constructor.new(_5965.FaceGearCompoundDynamicAnalysis))
        return value

    @property
    def face_meshes_compound_dynamic_analysis(self) -> 'List[_5966.FaceGearMeshCompoundDynamicAnalysis]':
        '''List[FaceGearMeshCompoundDynamicAnalysis]: 'FaceMeshesCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundDynamicAnalysis, constructor.new(_5966.FaceGearMeshCompoundDynamicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5846.FaceGearSetDynamicAnalysis]':
        '''List[FaceGearSetDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5846.FaceGearSetDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_5846.FaceGearSetDynamicAnalysis]':
        '''List[FaceGearSetDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_5846.FaceGearSetDynamicAnalysis))
        return value
