'''_5425.py

BoltedJointSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model import _1988
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6065
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _5500
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'BoltedJointSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointSingleMeshWhineAnalysis',)


class BoltedJointSingleMeshWhineAnalysis(_5500.SpecialisedAssemblySingleMeshWhineAnalysis):
    '''BoltedJointSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1988.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1988.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6065.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6065.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
