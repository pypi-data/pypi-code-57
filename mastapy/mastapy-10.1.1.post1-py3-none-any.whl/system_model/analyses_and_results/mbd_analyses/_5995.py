'''_5995.py

PointLoadMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _1933
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2295
from mastapy.system_model.analyses_and_results.mbd_analyses import _6034
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'PointLoadMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadMultiBodyDynamicsAnalysis',)


class PointLoadMultiBodyDynamicsAnalysis(_6034.VirtualComponentMultiBodyDynamicsAnalysis):
    '''PointLoadMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1933.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1933.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2295.PointLoadLoadCase':
        '''PointLoadLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2295.PointLoadLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
