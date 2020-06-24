'''_4716.py

BoltedJointModalAnalysis
'''


from mastapy.system_model.part_model import _1988
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6065
from mastapy.system_model.analyses_and_results.system_deflections import _2224
from mastapy.system_model.analyses_and_results.modal_analyses import _4797
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'BoltedJointModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointModalAnalysis',)


class BoltedJointModalAnalysis(_4797.SpecialisedAssemblyModalAnalysis):
    '''BoltedJointModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointModalAnalysis.TYPE'):
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

    @property
    def system_deflection_results(self) -> '_2224.BoltedJointSystemDeflection':
        '''BoltedJointSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2224.BoltedJointSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
