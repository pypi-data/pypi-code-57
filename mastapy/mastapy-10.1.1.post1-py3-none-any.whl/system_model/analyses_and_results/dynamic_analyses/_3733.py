'''_3733.py

StraightBevelPlanetGearDynamicAnalysis
'''


from mastapy.system_model.part_model.gears import _2010
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3729
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_PLANET_GEAR_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'StraightBevelPlanetGearDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelPlanetGearDynamicAnalysis',)


class StraightBevelPlanetGearDynamicAnalysis(_3729.StraightBevelDiffGearDynamicAnalysis):
    '''StraightBevelPlanetGearDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_PLANET_GEAR_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelPlanetGearDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2010.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2010.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
