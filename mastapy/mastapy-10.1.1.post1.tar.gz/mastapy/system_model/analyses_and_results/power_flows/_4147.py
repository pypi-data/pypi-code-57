'''_4147.py

ConnectionPowerFlow
'''


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _1764, _1760, _1780, _1765,
    _1761, _1776
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1794, _1798, _1800, _1818,
    _1804, _1790, _1812, _1814,
    _1816, _1820, _1808, _1809
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1822, _1824, _1828, _1830
)
from mastapy.system_model.analyses_and_results.power_flows import _4901
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2215, _2142, _2221, _2211,
    _2154, _2160, _2229, _2231,
    _2163, _2235, _2257, _2245,
    _2144, _2253, _2237, _2255,
    _2259, _2249, _2251, _2373,
    _2243, _2157, _2219
)
from mastapy.system_model.analyses_and_results.analysis_cases import _3375
from mastapy._internal.python_net import python_net_import

_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionPowerFlow',)


class ConnectionPowerFlow(_3375.ConnectionStaticLoadAnalysisCase):
    '''ConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_POWER_FLOW
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def is_loaded(self) -> 'bool':
        '''bool: 'IsLoaded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsLoaded

    @property
    def component_design(self) -> '_1764.Connection':
        '''Connection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1764.Connection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_belt_connection(self) -> '_1760.BeltConnection':
        '''BeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BeltConnection':
            raise CastException('Failed to cast component_design to BeltConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1760.BeltConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring_connection(self) -> '_1780.RollingRingConnection':
        '''RollingRingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'RollingRingConnection':
            raise CastException('Failed to cast component_design to RollingRingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1780.RollingRingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt_belt_connection(self) -> '_1765.CVTBeltConnection':
        '''CVTBeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CVTBeltConnection':
            raise CastException('Failed to cast component_design to CVTBeltConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1765.CVTBeltConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear_mesh(self) -> '_1794.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ConceptGearMesh':
            raise CastException('Failed to cast component_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1794.ConceptGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear_mesh(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CylindricalGearMesh':
            raise CastException('Failed to cast component_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear_mesh(self) -> '_1800.FaceGearMesh':
        '''FaceGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'FaceGearMesh':
            raise CastException('Failed to cast component_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1800.FaceGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear_mesh(self) -> '_1818.WormGearMesh':
        '''WormGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'WormGearMesh':
            raise CastException('Failed to cast component_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1818.WormGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear_mesh(self) -> '_1804.HypoidGearMesh':
        '''HypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'HypoidGearMesh':
            raise CastException('Failed to cast component_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1804.HypoidGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear_mesh(self) -> '_1790.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialGearMesh':
            raise CastException('Failed to cast component_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1790.BevelDifferentialGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear_mesh(self) -> '_1812.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SpiralBevelGearMesh':
            raise CastException('Failed to cast component_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1812.SpiralBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelDiffGearMesh':
            raise CastException('Failed to cast component_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear_mesh(self) -> '_1816.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelGearMesh':
            raise CastException('Failed to cast component_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1816.StraightBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear_mesh(self) -> '_1820.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ZerolBevelGearMesh':
            raise CastException('Failed to cast component_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1820.ZerolBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1808.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearMesh':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1808.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearMesh':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch_connection(self) -> '_1822.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ClutchConnection':
            raise CastException('Failed to cast component_design to ClutchConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1822.ClutchConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling_connection(self) -> '_1824.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ConceptCouplingConnection':
            raise CastException('Failed to cast component_design to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1824.ConceptCouplingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper_connection(self) -> '_1828.SpringDamperConnection':
        '''SpringDamperConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SpringDamperConnection':
            raise CastException('Failed to cast component_design to SpringDamperConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1828.SpringDamperConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_connection(self) -> '_1830.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'TorqueConverterConnection':
            raise CastException('Failed to cast component_design to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1830.TorqueConverterConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coaxial_connection(self) -> '_1761.CoaxialConnection':
        '''CoaxialConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CoaxialConnection':
            raise CastException('Failed to cast component_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1761.CoaxialConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_planetary_connection(self) -> '_1776.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'PlanetaryConnection':
            raise CastException('Failed to cast component_design to PlanetaryConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1776.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1764.Connection':
        '''Connection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1764.Connection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_belt_connection(self) -> '_1760.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'BeltConnection':
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1760.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_rolling_ring_connection(self) -> '_1780.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'RollingRingConnection':
            raise CastException('Failed to cast connection_design to RollingRingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1780.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cvt_belt_connection(self) -> '_1765.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'CVTBeltConnection':
            raise CastException('Failed to cast connection_design to CVTBeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1765.CVTBeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_gear_mesh(self) -> '_1794.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'ConceptGearMesh':
            raise CastException('Failed to cast connection_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1794.ConceptGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cylindrical_gear_mesh(self) -> '_1798.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'CylindricalGearMesh':
            raise CastException('Failed to cast connection_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1798.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_face_gear_mesh(self) -> '_1800.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'FaceGearMesh':
            raise CastException('Failed to cast connection_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1800.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_worm_gear_mesh(self) -> '_1818.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'WormGearMesh':
            raise CastException('Failed to cast connection_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1818.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_hypoid_gear_mesh(self) -> '_1804.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'HypoidGearMesh':
            raise CastException('Failed to cast connection_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1804.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_1790.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'BevelDifferentialGearMesh':
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1790.BevelDifferentialGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_1812.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'SpiralBevelGearMesh':
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1812.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_1814.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'StraightBevelDiffGearMesh':
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1814.StraightBevelDiffGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_1816.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'StraightBevelGearMesh':
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1816.StraightBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_1820.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'ZerolBevelGearMesh':
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1820.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1808.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearMesh':
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1808.KlingelnbergCycloPalloidHypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearMesh':
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1809.KlingelnbergCycloPalloidSpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_clutch_connection(self) -> '_1822.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'ClutchConnection':
            raise CastException('Failed to cast connection_design to ClutchConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1822.ClutchConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_coupling_connection(self) -> '_1824.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'ConceptCouplingConnection':
            raise CastException('Failed to cast connection_design to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1824.ConceptCouplingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spring_damper_connection(self) -> '_1828.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'SpringDamperConnection':
            raise CastException('Failed to cast connection_design to SpringDamperConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1828.SpringDamperConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_torque_converter_connection(self) -> '_1830.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'TorqueConverterConnection':
            raise CastException('Failed to cast connection_design to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1830.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_coaxial_connection(self) -> '_1761.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'CoaxialConnection':
            raise CastException('Failed to cast connection_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1761.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_planetary_connection(self) -> '_1776.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ConnectionDesign.__class__.__qualname__ != 'PlanetaryConnection':
            raise CastException('Failed to cast connection_design to PlanetaryConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new(_1776.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def power_flow(self) -> '_4901.PowerFlow':
        '''PowerFlow: 'PowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_4901.PowerFlow)(self.wrapped.PowerFlow) if self.wrapped.PowerFlow else None

    @property
    def torsional_system_deflection_analysis(self) -> '_2215.ConnectionSystemDeflection':
        '''ConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2215.ConnectionSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_belt_connection_system_deflection(self) -> '_2142.BeltConnectionSystemDeflection':
        '''BeltConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'BeltConnectionSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to BeltConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2142.BeltConnectionSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_rolling_ring_connection_system_deflection(self) -> '_2221.RollingRingConnectionSystemDeflection':
        '''RollingRingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'RollingRingConnectionSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to RollingRingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2221.RollingRingConnectionSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cvt_belt_connection_system_deflection(self) -> '_2211.CVTBeltConnectionSystemDeflection':
        '''CVTBeltConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'CVTBeltConnectionSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to CVTBeltConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2211.CVTBeltConnectionSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_clutch_connection_system_deflection(self) -> '_2154.ClutchConnectionSystemDeflection':
        '''ClutchConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'ClutchConnectionSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to ClutchConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2154.ClutchConnectionSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_concept_coupling_connection_system_deflection(self) -> '_2160.ConceptCouplingConnectionSystemDeflection':
        '''ConceptCouplingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'ConceptCouplingConnectionSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConceptCouplingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2160.ConceptCouplingConnectionSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_spring_damper_connection_system_deflection(self) -> '_2229.SpringDamperConnectionSystemDeflection':
        '''SpringDamperConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'SpringDamperConnectionSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to SpringDamperConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2229.SpringDamperConnectionSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_torque_converter_connection_system_deflection(self) -> '_2231.TorqueConverterConnectionSystemDeflection':
        '''TorqueConverterConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'TorqueConverterConnectionSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to TorqueConverterConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2231.TorqueConverterConnectionSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_concept_gear_mesh_system_deflection(self) -> '_2163.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'ConceptGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConceptGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2163.ConceptGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_face_gear_mesh_system_deflection(self) -> '_2235.FaceGearMeshSystemDeflection':
        '''FaceGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'FaceGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to FaceGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2235.FaceGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_worm_gear_mesh_system_deflection(self) -> '_2257.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'WormGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to WormGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2257.WormGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_hypoid_gear_mesh_system_deflection(self) -> '_2245.HypoidGearMeshSystemDeflection':
        '''HypoidGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'HypoidGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to HypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2245.HypoidGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_bevel_differential_gear_mesh_system_deflection(self) -> '_2144.BevelDifferentialGearMeshSystemDeflection':
        '''BevelDifferentialGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'BevelDifferentialGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to BevelDifferentialGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2144.BevelDifferentialGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_spiral_bevel_gear_mesh_system_deflection(self) -> '_2253.SpiralBevelGearMeshSystemDeflection':
        '''SpiralBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'SpiralBevelGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to SpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2253.SpiralBevelGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_straight_bevel_diff_gear_mesh_system_deflection(self) -> '_2237.StraightBevelDiffGearMeshSystemDeflection':
        '''StraightBevelDiffGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'StraightBevelDiffGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to StraightBevelDiffGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2237.StraightBevelDiffGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_straight_bevel_gear_mesh_system_deflection(self) -> '_2255.StraightBevelGearMeshSystemDeflection':
        '''StraightBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'StraightBevelGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to StraightBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2255.StraightBevelGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_zerol_bevel_gear_mesh_system_deflection(self) -> '_2259.ZerolBevelGearMeshSystemDeflection':
        '''ZerolBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'ZerolBevelGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to ZerolBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2259.ZerolBevelGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(self) -> '_2249.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2249.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(self) -> '_2251.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2251.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2373.CylindricalGearMeshSystemDeflectionTimestep':
        '''CylindricalGearMeshSystemDeflectionTimestep: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'CylindricalGearMeshSystemDeflectionTimestep':
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2373.CylindricalGearMeshSystemDeflectionTimestep)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2243.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        '''CylindricalGearMeshSystemDeflectionWithLTCAResults: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'CylindricalGearMeshSystemDeflectionWithLTCAResults':
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2243.CylindricalGearMeshSystemDeflectionWithLTCAResults)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_coaxial_connection_system_deflection(self) -> '_2157.CoaxialConnectionSystemDeflection':
        '''CoaxialConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'CoaxialConnectionSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to CoaxialConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2157.CoaxialConnectionSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_planetary_connection_system_deflection(self) -> '_2219.PlanetaryConnectionSystemDeflection':
        '''PlanetaryConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__ != 'PlanetaryConnectionSystemDeflection':
            raise CastException('Failed to cast torsional_system_deflection_analysis to PlanetaryConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new(_2219.PlanetaryConnectionSystemDeflection)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None
