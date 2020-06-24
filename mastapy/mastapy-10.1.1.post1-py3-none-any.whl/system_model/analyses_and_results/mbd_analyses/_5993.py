'''_5993.py

PlanetaryGearSetMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.gears import _1986
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5952
from mastapy._internal.python_net import python_net_import

_PLANETARY_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'PlanetaryGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryGearSetMultiBodyDynamicsAnalysis',)


class PlanetaryGearSetMultiBodyDynamicsAnalysis(_5952.CylindricalGearSetMultiBodyDynamicsAnalysis):
    '''PlanetaryGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1986.PlanetaryGearSet':
        '''PlanetaryGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1986.PlanetaryGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
