'''_2344.py

ZerolBevelGearSetSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2093
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6214
from mastapy.system_model.analyses_and_results.power_flows import _3340
from mastapy.gears.rating.zerol_bevel import _173
from mastapy.system_model.analyses_and_results.system_deflections import _2345, _2343, _2222
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ZerolBevelGearSetSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetSystemDeflection',)


class ZerolBevelGearSetSystemDeflection(_2222.BevelGearSetSystemDeflection):
    '''ZerolBevelGearSetSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2093.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2093.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6214.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6214.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3340.ZerolBevelGearSetPowerFlow':
        '''ZerolBevelGearSetPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3340.ZerolBevelGearSetPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def rating(self) -> '_173.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_173.ZerolBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_173.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_173.ZerolBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def zerol_bevel_gears_system_deflection(self) -> 'List[_2345.ZerolBevelGearSystemDeflection]':
        '''List[ZerolBevelGearSystemDeflection]: 'ZerolBevelGearsSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsSystemDeflection, constructor.new(_2345.ZerolBevelGearSystemDeflection))
        return value

    @property
    def zerol_bevel_meshes_system_deflection(self) -> 'List[_2343.ZerolBevelGearMeshSystemDeflection]':
        '''List[ZerolBevelGearMeshSystemDeflection]: 'ZerolBevelMeshesSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesSystemDeflection, constructor.new(_2343.ZerolBevelGearMeshSystemDeflection))
        return value
