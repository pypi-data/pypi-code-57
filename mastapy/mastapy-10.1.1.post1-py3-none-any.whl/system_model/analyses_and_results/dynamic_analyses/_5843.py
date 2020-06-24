'''_5843.py

ExternalCADModelDynamicAnalysis
'''


from mastapy.system_model.part_model import _1996
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6112
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5818
from mastapy._internal.python_net import python_net_import

_EXTERNAL_CAD_MODEL_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'ExternalCADModelDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ExternalCADModelDynamicAnalysis',)


class ExternalCADModelDynamicAnalysis(_5818.ComponentDynamicAnalysis):
    '''ExternalCADModelDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _EXTERNAL_CAD_MODEL_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ExternalCADModelDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1996.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1996.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6112.ExternalCADModelLoadCase':
        '''ExternalCADModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6112.ExternalCADModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
