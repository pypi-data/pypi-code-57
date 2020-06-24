'''_5086.py

SynchroniserHalfMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2137
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6193
from mastapy.system_model.analyses_and_results.mbd_analyses import _5088
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_HALF_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'SynchroniserHalfMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserHalfMultiBodyDynamicsAnalysis',)


class SynchroniserHalfMultiBodyDynamicsAnalysis(_5088.SynchroniserPartMultiBodyDynamicsAnalysis):
    '''SynchroniserHalfMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_HALF_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserHalfMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2137.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2137.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6193.SynchroniserHalfLoadCase':
        '''SynchroniserHalfLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6193.SynchroniserHalfLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
