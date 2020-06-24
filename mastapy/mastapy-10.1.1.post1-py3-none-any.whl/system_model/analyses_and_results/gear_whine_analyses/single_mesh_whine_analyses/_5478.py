'''_5478.py

MeasurementComponentSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _2005
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6149
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5524
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'MeasurementComponentSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentSingleMeshWhineAnalysis',)


class MeasurementComponentSingleMeshWhineAnalysis(_5524.VirtualComponentSingleMeshWhineAnalysis):
    '''MeasurementComponentSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2005.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2005.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6149.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6149.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
