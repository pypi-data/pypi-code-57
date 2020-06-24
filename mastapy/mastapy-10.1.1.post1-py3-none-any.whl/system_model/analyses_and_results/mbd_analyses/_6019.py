'''_6019.py

StraightBevelGearMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.gears import _2006
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _2361
from mastapy.system_model.analyses_and_results.mbd_analyses import _5924
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'StraightBevelGearMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearMultiBodyDynamicsAnalysis',)


class StraightBevelGearMultiBodyDynamicsAnalysis(_5924.BevelGearMultiBodyDynamicsAnalysis):
    '''StraightBevelGearMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2006.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2006.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_2361.StraightBevelGearLoadCase':
        '''StraightBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2361.StraightBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
