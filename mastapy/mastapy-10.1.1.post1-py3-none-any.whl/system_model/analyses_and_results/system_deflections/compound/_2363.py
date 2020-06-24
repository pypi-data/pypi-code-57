'''_2363.py

BeltDriveCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2111
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2215
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2446
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'BeltDriveCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveCompoundSystemDeflection',)


class BeltDriveCompoundSystemDeflection(_2446.SpecialisedAssemblyCompoundSystemDeflection):
    '''BeltDriveCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveCompoundSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2111.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.BeltDrive)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2111.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2111.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2215.BeltDriveSystemDeflection]':
        '''List[BeltDriveSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2215.BeltDriveSystemDeflection))
        return value

    @property
    def assembly_system_deflection_load_cases(self) -> 'List[_2215.BeltDriveSystemDeflection]':
        '''List[BeltDriveSystemDeflection]: 'AssemblySystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionLoadCases, constructor.new(_2215.BeltDriveSystemDeflection))
        return value
