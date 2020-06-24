'''_3051.py

FaceGearSetCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1978
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3050, _3125, _3066
from mastapy.system_model.analyses_and_results.modal_analyses import _3939
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'FaceGearSetCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundModalAnalysis',)


class FaceGearSetCompoundModalAnalysis(_3066.GearSetCompoundModalAnalysis):
    '''FaceGearSetCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1978.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1978.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1978.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1978.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_modal_analysis(self) -> 'List[_3050.FaceGearCompoundModalAnalysis]':
        '''List[FaceGearCompoundModalAnalysis]: 'FaceGearsCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundModalAnalysis, constructor.new(_3050.FaceGearCompoundModalAnalysis))
        return value

    @property
    def face_meshes_compound_modal_analysis(self) -> 'List[_3125.FaceGearMeshCompoundModalAnalysis]':
        '''List[FaceGearMeshCompoundModalAnalysis]: 'FaceMeshesCompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundModalAnalysis, constructor.new(_3125.FaceGearMeshCompoundModalAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3939.FaceGearSetModalAnalysis]':
        '''List[FaceGearSetModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3939.FaceGearSetModalAnalysis))
        return value

    @property
    def assembly_modal_analysis_load_cases(self) -> 'List[_3939.FaceGearSetModalAnalysis]':
        '''List[FaceGearSetModalAnalysis]: 'AssemblyModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisLoadCases, constructor.new(_3939.FaceGearSetModalAnalysis))
        return value
