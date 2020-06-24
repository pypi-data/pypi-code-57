'''_6095.py

FaceGearCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1997
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses import _5957
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _6099
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'FaceGearCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundMultiBodyDynamicsAnalysis',)


class FaceGearCompoundMultiBodyDynamicsAnalysis(_6099.GearCompoundMultiBodyDynamicsAnalysis):
    '''FaceGearCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1997.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1997.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5957.FaceGearMultiBodyDynamicsAnalysis]':
        '''List[FaceGearMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5957.FaceGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def component_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5957.FaceGearMultiBodyDynamicsAnalysis]':
        '''List[FaceGearMultiBodyDynamicsAnalysis]: 'ComponentMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5957.FaceGearMultiBodyDynamicsAnalysis))
        return value
