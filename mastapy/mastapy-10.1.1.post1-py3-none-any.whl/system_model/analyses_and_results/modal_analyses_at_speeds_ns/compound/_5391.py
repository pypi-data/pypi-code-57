'''_5391.py

SynchroniserCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.couplings import _1976
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5274
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import _5376
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'SynchroniserCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserCompoundModalAnalysesAtSpeeds',)


class SynchroniserCompoundModalAnalysesAtSpeeds(_5376.SpecialisedAssemblyCompoundModalAnalysesAtSpeeds):
    '''SynchroniserCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_COMPOUND_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserCompoundModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1976.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1976.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1976.Synchroniser':
        '''Synchroniser: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1976.Synchroniser)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5274.SynchroniserModalAnalysesAtSpeeds]':
        '''List[SynchroniserModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5274.SynchroniserModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_5274.SynchroniserModalAnalysesAtSpeeds]':
        '''List[SynchroniserModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_5274.SynchroniserModalAnalysesAtSpeeds))
        return value
