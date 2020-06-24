'''_5726.py

RollingRingAssemblyModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.couplings import _1975
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2192
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _5733
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'RollingRingAssemblyModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyModalAnalysisAtASpeed',)


class RollingRingAssemblyModalAnalysisAtASpeed(_5733.SpecialisedAssemblyModalAnalysisAtASpeed):
    '''RollingRingAssemblyModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_MODAL_ANALYSIS_AT_A_SPEED
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1975.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1975.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2192.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None
