'''_4985.py

BoltedJointMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _1988
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6065
from mastapy.system_model.analyses_and_results.mbd_analyses import _5071
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BoltedJointMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointMultiBodyDynamicsAnalysis',)


class BoltedJointMultiBodyDynamicsAnalysis(_5071.SpecialisedAssemblyMultiBodyDynamicsAnalysis):
    '''BoltedJointMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointMultiBodyDynamicsAnalysis.TYPE'):
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
