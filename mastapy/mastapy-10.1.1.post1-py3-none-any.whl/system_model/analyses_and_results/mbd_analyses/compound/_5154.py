'''_5154.py

CylindricalGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2065
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5152, _5153, _5164
from mastapy.system_model.analyses_and_results.mbd_analyses import _5012
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'CylindricalGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundMultiBodyDynamicsAnalysis',)


class CylindricalGearSetCompoundMultiBodyDynamicsAnalysis(_5164.GearSetCompoundMultiBodyDynamicsAnalysis):
    '''CylindricalGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2065.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2065.CylindricalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2065.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2065.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def cylindrical_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_5152.CylindricalGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearCompoundMultiBodyDynamicsAnalysis]: 'CylindricalGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_5152.CylindricalGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_5153.CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis]: 'CylindricalMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_5153.CylindricalGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5012.CylindricalGearSetMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5012.CylindricalGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5012.CylindricalGearSetMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5012.CylindricalGearSetMultiBodyDynamicsAnalysis))
        return value
