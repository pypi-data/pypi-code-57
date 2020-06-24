'''_3277.py

PlanetCarrierCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1932
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _3927
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _3274
from mastapy._internal.python_net import python_net_import

_PLANET_CARRIER_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'PlanetCarrierCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetCarrierCompoundModalAnalysis',)


class PlanetCarrierCompoundModalAnalysis(_3274.MountableComponentCompoundModalAnalysis):
    '''PlanetCarrierCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANET_CARRIER_COMPOUND_MODAL_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetCarrierCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1932.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1932.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3927.PlanetCarrierModalAnalysis]':
        '''List[PlanetCarrierModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3927.PlanetCarrierModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_3927.PlanetCarrierModalAnalysis]':
        '''List[PlanetCarrierModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_3927.PlanetCarrierModalAnalysis))
        return value
