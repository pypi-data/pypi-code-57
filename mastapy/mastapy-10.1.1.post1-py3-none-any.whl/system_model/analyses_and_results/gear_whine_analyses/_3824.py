'''_3824.py

BevelDifferentialGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _1981
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2316
from mastapy.system_model.analyses_and_results.system_deflections import _2145
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _3823, _3774, _3828
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'BevelDifferentialGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetGearWhineAnalysis',)


class BevelDifferentialGearSetGearWhineAnalysis(_3828.BevelGearSetGearWhineAnalysis):
    '''BevelDifferentialGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_GEAR_WHINE_ANALYSIS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1981.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1981.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2316.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2316.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2145.BevelDifferentialGearSetSystemDeflection':
        '''BevelDifferentialGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2145.BevelDifferentialGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def bevel_differential_gears_gear_whine_analysis(self) -> 'List[_3823.BevelDifferentialGearGearWhineAnalysis]':
        '''List[BevelDifferentialGearGearWhineAnalysis]: 'BevelDifferentialGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsGearWhineAnalysis, constructor.new(_3823.BevelDifferentialGearGearWhineAnalysis))
        return value

    @property
    def bevel_differential_meshes_gear_whine_analysis(self) -> 'List[_3774.BevelDifferentialGearMeshGearWhineAnalysis]':
        '''List[BevelDifferentialGearMeshGearWhineAnalysis]: 'BevelDifferentialMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesGearWhineAnalysis, constructor.new(_3774.BevelDifferentialGearMeshGearWhineAnalysis))
        return value
