'''_6013.py

SpringDamperHalfMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2019
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2196
from mastapy.system_model.analyses_and_results.mbd_analyses import _5945
from mastapy._internal.python_net import python_net_import

_SPRING_DAMPER_HALF_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'SpringDamperHalfMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpringDamperHalfMultiBodyDynamicsAnalysis',)


class SpringDamperHalfMultiBodyDynamicsAnalysis(_5945.CouplingHalfMultiBodyDynamicsAnalysis):
    '''SpringDamperHalfMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPRING_DAMPER_HALF_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpringDamperHalfMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2019.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2019.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2196.SpringDamperHalfLoadCase':
        '''SpringDamperHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2196.SpringDamperHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
