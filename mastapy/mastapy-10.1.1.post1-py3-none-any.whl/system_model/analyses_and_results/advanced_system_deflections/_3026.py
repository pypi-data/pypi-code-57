'''_3026.py

BeltDriveAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2029
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _2237
from mastapy.system_model.analyses_and_results.system_deflections import _2144
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3100
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'BeltDriveAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveAdvancedSystemDeflection',)


class BeltDriveAdvancedSystemDeflection(_3100.SpecialisedAssemblyAdvancedSystemDeflection):
    '''BeltDriveAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2029.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2029.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_2237.BeltDriveLoadCase':
        '''BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2237.BeltDriveLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2144.BeltDriveSystemDeflection]':
        '''List[BeltDriveSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2144.BeltDriveSystemDeflection))
        return value
