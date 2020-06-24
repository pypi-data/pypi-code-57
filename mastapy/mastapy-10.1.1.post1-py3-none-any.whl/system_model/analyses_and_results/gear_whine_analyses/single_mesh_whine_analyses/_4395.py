'''_4395.py

StraightBevelSunGearSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2011
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4390
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'StraightBevelSunGearSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearSingleMeshWhineAnalysis',)


class StraightBevelSunGearSingleMeshWhineAnalysis(_4390.StraightBevelDiffGearSingleMeshWhineAnalysis):
    '''StraightBevelSunGearSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2011.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2011.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
