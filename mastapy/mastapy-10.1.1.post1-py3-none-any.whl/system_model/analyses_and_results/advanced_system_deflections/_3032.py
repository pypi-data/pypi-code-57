'''_3032.py

CouplingHalfAdvancedSystemDeflection
'''


from mastapy.system_model.part_model.couplings import (
    _2038, _2039, _2040, _2041,
    _2042, _2043, _2045, _2046,
    _2047, _2048, _2049
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3093
from mastapy._internal.python_net import python_net_import

_COUPLING_HALF_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'CouplingHalfAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('CouplingHalfAdvancedSystemDeflection',)


class CouplingHalfAdvancedSystemDeflection(_3093.MountableComponentAdvancedSystemDeflection):
    '''CouplingHalfAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _COUPLING_HALF_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CouplingHalfAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2038.CouplingHalf':
        '''CouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2038.CouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch_half(self) -> '_2039.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ClutchHalf':
            raise CastException('Failed to cast component_design to ClutchHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2039.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling_half(self) -> '_2040.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ConceptCouplingHalf':
            raise CastException('Failed to cast component_design to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2040.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_pulley(self) -> '_2041.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Pulley':
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2041.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring(self) -> '_2042.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'RollingRing':
            raise CastException('Failed to cast component_design to RollingRing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2042.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper_half(self) -> '_2043.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SpringDamperHalf':
            raise CastException('Failed to cast component_design to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2043.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_pump(self) -> '_2045.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'TorqueConverterPump':
            raise CastException('Failed to cast component_design to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2045.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_turbine(self) -> '_2046.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'TorqueConverterTurbine':
            raise CastException('Failed to cast component_design to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2046.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt_pulley(self) -> '_2047.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CVTPulley':
            raise CastException('Failed to cast component_design to CVTPulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2047.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_half(self) -> '_2048.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SynchroniserHalf':
            raise CastException('Failed to cast component_design to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2048.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_sleeve(self) -> '_2049.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SynchroniserSleeve':
            raise CastException('Failed to cast component_design to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2049.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
