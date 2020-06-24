'''_3485.py

PlanetaryGearSetDynamicAnalysis
'''


from mastapy.system_model.part_model.gears import _2001
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.dynamic_analyses import _3473
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'PlanetaryGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetDynamicAnalysis',)


class PlanetaryGearSetDynamicAnalysis(_3473.CylindricalGearSetDynamicAnalysis):
    '''PlanetaryGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_DYNAMIC_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2001.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2001.PlanetaryGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
