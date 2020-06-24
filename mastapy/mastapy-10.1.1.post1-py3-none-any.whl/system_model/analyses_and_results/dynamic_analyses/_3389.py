'''_3389.py

PulleyDynamicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2041
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2246
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3386
from mastapy._internal.python_net import python_net_import

_PULLEY_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'PulleyDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PulleyDynamicAnalysis',)


class PulleyDynamicAnalysis(_3386.CouplingHalfDynamicAnalysis):
    '''PulleyDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PULLEY_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PulleyDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2041.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2041.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2246.PulleyLoadCase':
        '''PulleyLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2246.PulleyLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
