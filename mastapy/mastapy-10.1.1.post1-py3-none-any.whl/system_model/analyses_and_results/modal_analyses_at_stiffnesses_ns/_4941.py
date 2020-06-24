'''_4941.py

BoltedJointModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model import _1911
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2267
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _5016
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'BoltedJointModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointModalAnalysesAtStiffnesses',)


class BoltedJointModalAnalysesAtStiffnesses(_5016.SpecialisedAssemblyModalAnalysesAtStiffnesses):
    '''BoltedJointModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_MODAL_ANALYSES_AT_STIFFNESSES
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1911.BoltedJoint':
        '''BoltedJoint: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1911.BoltedJoint)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2267.BoltedJointLoadCase':
        '''BoltedJointLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2267.BoltedJointLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
