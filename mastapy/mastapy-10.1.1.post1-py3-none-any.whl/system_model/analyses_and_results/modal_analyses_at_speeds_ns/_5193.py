'''_5193.py

ConceptCouplingModalAnalysesAtSpeeds
'''


from mastapy.system_model.part_model.couplings import _1989
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2175
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _5204
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ConceptCouplingModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingModalAnalysesAtSpeeds',)


class ConceptCouplingModalAnalysesAtSpeeds(_5204.CouplingModalAnalysesAtSpeeds):
    '''ConceptCouplingModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_MODAL_ANALYSES_AT_SPEEDS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1989.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2175.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2175.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
