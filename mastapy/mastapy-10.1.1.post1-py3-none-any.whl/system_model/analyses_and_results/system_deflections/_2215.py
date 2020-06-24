'''_2215.py

BeltDriveSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2111
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6056
from mastapy.system_model.analyses_and_results.power_flows import _3224
from mastapy.system_model.analyses_and_results.system_deflections import _2214, _2310
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'BeltDriveSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveSystemDeflection',)


class BeltDriveSystemDeflection(_2310.SpecialisedAssemblySystemDeflection):
    '''BeltDriveSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2111.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6056.BeltDriveLoadCase':
        '''BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6056.BeltDriveLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3224.BeltDrivePowerFlow':
        '''BeltDrivePowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3224.BeltDrivePowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def belts(self) -> 'List[_2214.BeltConnectionSystemDeflection]':
        '''List[BeltConnectionSystemDeflection]: 'Belts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Belts, constructor.new(_2214.BeltConnectionSystemDeflection))
        return value
