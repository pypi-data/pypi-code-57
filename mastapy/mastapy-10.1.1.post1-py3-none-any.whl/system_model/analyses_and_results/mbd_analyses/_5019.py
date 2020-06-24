'''_5019.py

FlexiblePinAssemblyMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _1997
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6116
from mastapy.system_model.analyses_and_results.mbd_analyses import _5071
from mastapy._internal.python_net import python_net_import

_FLEXIBLE_PIN_ASSEMBLY_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'FlexiblePinAssemblyMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FlexiblePinAssemblyMultiBodyDynamicsAnalysis',)


class FlexiblePinAssemblyMultiBodyDynamicsAnalysis(_5071.SpecialisedAssemblyMultiBodyDynamicsAnalysis):
    '''FlexiblePinAssemblyMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _FLEXIBLE_PIN_ASSEMBLY_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FlexiblePinAssemblyMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1997.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1997.FlexiblePinAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6116.FlexiblePinAssemblyLoadCase':
        '''FlexiblePinAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6116.FlexiblePinAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
