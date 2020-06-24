'''_4225.py

SpringDamperHalfSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2028
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2196
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4217
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'SpringDamperHalfSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfSingleMeshWhineAnalysis',)


class SpringDamperHalfSingleMeshWhineAnalysis(_4217.CouplingHalfSingleMeshWhineAnalysis):
    '''SpringDamperHalfSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2028.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2028.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2196.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
