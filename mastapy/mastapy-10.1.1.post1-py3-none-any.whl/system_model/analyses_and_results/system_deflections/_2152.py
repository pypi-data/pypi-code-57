'''_2152.py

BoltedJointSystemDeflection
'''


from mastapy.system_model.part_model import _1911
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2267
from mastapy.system_model.analyses_and_results.system_deflections import _2300
from mastapy._internal.python_net import python_net_import

_BOLTED_JOINT_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'BoltedJointSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BoltedJointSystemDeflection',)


class BoltedJointSystemDeflection(_2300.SpecialisedAssemblySystemDeflection):
    '''BoltedJointSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BOLTED_JOINT_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BoltedJointSystemDeflection.TYPE'):
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
