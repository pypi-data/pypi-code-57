'''_5492.py

RollingRingAssemblySingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.couplings import _2131
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6169
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5500
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'RollingRingAssemblySingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblySingleMeshWhineAnalysis',)


class RollingRingAssemblySingleMeshWhineAnalysis(_5500.SpecialisedAssemblySingleMeshWhineAnalysis):
    '''RollingRingAssemblySingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblySingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2131.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2131.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6169.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6169.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
