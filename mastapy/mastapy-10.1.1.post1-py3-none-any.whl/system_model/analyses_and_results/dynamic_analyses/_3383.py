'''_3383.py

ConceptCouplingDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2035
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2240
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3385
from mastapy._internal.python_net import python_net_import

_CONCEPT_COUPLING_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ConceptCouplingDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptCouplingDynamicAnalysis',)


class ConceptCouplingDynamicAnalysis(_3385.CouplingDynamicAnalysis):
    '''ConceptCouplingDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_COUPLING_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptCouplingDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2035.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2035.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2240.ConceptCouplingLoadCase':
        '''ConceptCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2240.ConceptCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
