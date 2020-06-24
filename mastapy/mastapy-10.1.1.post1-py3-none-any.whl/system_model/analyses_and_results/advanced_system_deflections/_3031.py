'''_3031.py

CouplingAdvancedSystemDeflection
'''


from mastapy.system_model.part_model.couplings import (
    _2030, _2034, _2035, _2036,
    _2037
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3100
from mastapy._internal.python_net import python_net_import

_COUPLING_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CouplingAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingAdvancedSystemDeflection',)


class CouplingAdvancedSystemDeflection(_3100.SpecialisedAssemblyAdvancedSystemDeflection):
    '''CouplingAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _COUPLING_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2030.Coupling':
        '''Coupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2030.Coupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_clutch(self) -> '_2034.Clutch':
        '''Clutch: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.AssemblyDesign.__class__.__qualname__ != 'Clutch':
            raise CastException('Failed to cast assembly_design to Clutch. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2034.Clutch)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_concept_coupling(self) -> '_2035.ConceptCoupling':
        '''ConceptCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.AssemblyDesign.__class__.__qualname__ != 'ConceptCoupling':
            raise CastException('Failed to cast assembly_design to ConceptCoupling. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2035.ConceptCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_spring_damper(self) -> '_2036.SpringDamper':
        '''SpringDamper: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.AssemblyDesign.__class__.__qualname__ != 'SpringDamper':
            raise CastException('Failed to cast assembly_design to SpringDamper. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2036.SpringDamper)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_design_of_type_torque_converter(self) -> '_2037.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.AssemblyDesign.__class__.__qualname__ != 'TorqueConverter':
            raise CastException('Failed to cast assembly_design to TorqueConverter. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new(_2037.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None
