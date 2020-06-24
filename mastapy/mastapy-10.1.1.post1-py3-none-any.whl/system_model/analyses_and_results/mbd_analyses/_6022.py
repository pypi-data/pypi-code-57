'''_6022.py

StraightBevelSunGearMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.gears import _2011
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _6016
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'StraightBevelSunGearMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearMultiBodyDynamicsAnalysis',)


class StraightBevelSunGearMultiBodyDynamicsAnalysis(_6016.StraightBevelDiffGearMultiBodyDynamicsAnalysis):
    '''StraightBevelSunGearMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2011.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
