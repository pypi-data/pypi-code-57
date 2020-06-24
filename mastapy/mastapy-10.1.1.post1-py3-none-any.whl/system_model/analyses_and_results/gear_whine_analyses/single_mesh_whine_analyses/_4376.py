'''_4376.py

CylindricalPlanetGearSingleMeshWhineAnalysis
'''


from mastapy.system_model.part_model.gears import _2014
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import _4374
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_PLANET_GEAR_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'CylindricalPlanetGearSingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalPlanetGearSingleMeshWhineAnalysis',)


class CylindricalPlanetGearSingleMeshWhineAnalysis(_4374.CylindricalGearSingleMeshWhineAnalysis):
    '''CylindricalPlanetGearSingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_PLANET_GEAR_SINGLE_MESH_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalPlanetGearSingleMeshWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2014.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2014.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
