'''_5426.py

BoltSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _1987
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6066
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5431
from mastapy._internal.python_net import python_net_import

_BOLT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'BoltSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltSingleMeshWhineAnalysis',)


class BoltSingleMeshWhineAnalysis(_5431.ComponentSingleMeshWhineAnalysis):
    '''BoltSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1987.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6066.BoltLoadCase':
        '''BoltLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6066.BoltLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
