'''_1763.py

ComponentMeasurer
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model import (
    _1912, _1910, _1916, _1919,
    _1921, _1924, _1932, _1908,
    _1929, _1926, _1927, _1933,
    _1934, _1938
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _1942
from mastapy.system_model.part_model.couplings import (
    _1967, _2015, _2016, _2017,
    _2018, _2019, _2021, _2022,
    _2023, _2024, _2025
)
from mastapy.system_model.part_model.gears import (
    _1994, _1996, _1997, _1998,
    _2002, _2003, _2004, _2005,
    _2006, _2007, _2008, _2009,
    _2010, _2011, _2012, _2013,
    _2014
)
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_COMPONENT_MEASURER = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ComponentMeasurer')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentMeasurer',)


class ComponentMeasurer(_1.APIBase):
    '''ComponentMeasurer

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_MEASURER
    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentMeasurer.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def offset_of_component(self) -> 'float':
        '''float: 'OffsetOfComponent' is the original name of this property.'''

        return self.wrapped.OffsetOfComponent

    @offset_of_component.setter
    def offset_of_component(self, value: 'float'):
        self.wrapped.OffsetOfComponent = float(value) if value else 0.0

    @property
    def component(self) -> '_1912.Component':
        '''Component: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1912.Component)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bolt(self) -> '_1910.Bolt':
        '''Bolt: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'Bolt':
            raise CastException('Failed to cast component to Bolt. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1910.Bolt)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_datum(self) -> '_1916.Datum':
        '''Datum: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'Datum':
            raise CastException('Failed to cast component to Datum. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1916.Datum)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_external_cad_model(self) -> '_1919.ExternalCADModel':
        '''ExternalCADModel: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'ExternalCADModel':
            raise CastException('Failed to cast component to ExternalCADModel. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1919.ExternalCADModel)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_guide_dxf_model(self) -> '_1921.GuideDxfModel':
        '''GuideDxfModel: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'GuideDxfModel':
            raise CastException('Failed to cast component to GuideDxfModel. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1921.GuideDxfModel)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_imported_fe_component(self) -> '_1924.ImportedFEComponent':
        '''ImportedFEComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'ImportedFEComponent':
            raise CastException('Failed to cast component to ImportedFEComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1924.ImportedFEComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_shaft(self) -> '_1942.Shaft':
        '''Shaft: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'Shaft':
            raise CastException('Failed to cast component to Shaft. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1942.Shaft)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_planet_carrier(self) -> '_1932.PlanetCarrier':
        '''PlanetCarrier: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'PlanetCarrier':
            raise CastException('Failed to cast component to PlanetCarrier. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1932.PlanetCarrier)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bearing(self) -> '_1908.Bearing':
        '''Bearing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'Bearing':
            raise CastException('Failed to cast component to Bearing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1908.Bearing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_oil_seal(self) -> '_1929.OilSeal':
        '''OilSeal: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'OilSeal':
            raise CastException('Failed to cast component to OilSeal. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1929.OilSeal)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_shaft_hub_connection(self) -> '_1967.ShaftHubConnection':
        '''ShaftHubConnection: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'ShaftHubConnection':
            raise CastException('Failed to cast component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1967.ShaftHubConnection)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_mass_disc(self) -> '_1926.MassDisc':
        '''MassDisc: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'MassDisc':
            raise CastException('Failed to cast component to MassDisc. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1926.MassDisc)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_measurement_component(self) -> '_1927.MeasurementComponent':
        '''MeasurementComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'MeasurementComponent':
            raise CastException('Failed to cast component to MeasurementComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1927.MeasurementComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_point_load(self) -> '_1933.PointLoad':
        '''PointLoad: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'PointLoad':
            raise CastException('Failed to cast component to PointLoad. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1933.PointLoad)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_power_load(self) -> '_1934.PowerLoad':
        '''PowerLoad: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'PowerLoad':
            raise CastException('Failed to cast component to PowerLoad. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1934.PowerLoad)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_unbalanced_mass(self) -> '_1938.UnbalancedMass':
        '''UnbalancedMass: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'UnbalancedMass':
            raise CastException('Failed to cast component to UnbalancedMass. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1938.UnbalancedMass)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_concept_gear(self) -> '_1994.ConceptGear':
        '''ConceptGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'ConceptGear':
            raise CastException('Failed to cast component to ConceptGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1994.ConceptGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cylindrical_gear(self) -> '_1996.CylindricalGear':
        '''CylindricalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'CylindricalGear':
            raise CastException('Failed to cast component to CylindricalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1996.CylindricalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_face_gear(self) -> '_1997.FaceGear':
        '''FaceGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'FaceGear':
            raise CastException('Failed to cast component to FaceGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1997.FaceGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_worm_gear(self) -> '_1998.WormGear':
        '''WormGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'WormGear':
            raise CastException('Failed to cast component to WormGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1998.WormGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_hypoid_gear(self) -> '_2002.HypoidGear':
        '''HypoidGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'HypoidGear':
            raise CastException('Failed to cast component to HypoidGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2002.HypoidGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_gear(self) -> '_2003.BevelDifferentialGear':
        '''BevelDifferentialGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'BevelDifferentialGear':
            raise CastException('Failed to cast component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2003.BevelDifferentialGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_spiral_bevel_gear(self) -> '_2004.SpiralBevelGear':
        '''SpiralBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'SpiralBevelGear':
            raise CastException('Failed to cast component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2004.SpiralBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_diff_gear(self) -> '_2005.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'StraightBevelDiffGear':
            raise CastException('Failed to cast component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2005.StraightBevelDiffGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_gear(self) -> '_2006.StraightBevelGear':
        '''StraightBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'StraightBevelGear':
            raise CastException('Failed to cast component to StraightBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2006.StraightBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_zerol_bevel_gear(self) -> '_2007.ZerolBevelGear':
        '''ZerolBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'ZerolBevelGear':
            raise CastException('Failed to cast component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2007.ZerolBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_planet_gear(self) -> '_2008.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'BevelDifferentialPlanetGear':
            raise CastException('Failed to cast component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2008.BevelDifferentialPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_sun_gear(self) -> '_2009.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'BevelDifferentialSunGear':
            raise CastException('Failed to cast component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2009.BevelDifferentialSunGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_planet_gear(self) -> '_2010.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'StraightBevelPlanetGear':
            raise CastException('Failed to cast component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2010.StraightBevelPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_sun_gear(self) -> '_2011.StraightBevelSunGear':
        '''StraightBevelSunGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'StraightBevelSunGear':
            raise CastException('Failed to cast component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2011.StraightBevelSunGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2012.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGear':
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2012.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2013.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGear':
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2013.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cylindrical_planet_gear(self) -> '_2014.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'CylindricalPlanetGear':
            raise CastException('Failed to cast component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2014.CylindricalPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_clutch_half(self) -> '_2015.ClutchHalf':
        '''ClutchHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'ClutchHalf':
            raise CastException('Failed to cast component to ClutchHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2015.ClutchHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_concept_coupling_half(self) -> '_2016.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'ConceptCouplingHalf':
            raise CastException('Failed to cast component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2016.ConceptCouplingHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_pulley(self) -> '_2017.Pulley':
        '''Pulley: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'Pulley':
            raise CastException('Failed to cast component to Pulley. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2017.Pulley)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_rolling_ring(self) -> '_2018.RollingRing':
        '''RollingRing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'RollingRing':
            raise CastException('Failed to cast component to RollingRing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2018.RollingRing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_spring_damper_half(self) -> '_2019.SpringDamperHalf':
        '''SpringDamperHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'SpringDamperHalf':
            raise CastException('Failed to cast component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2019.SpringDamperHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_torque_converter_pump(self) -> '_2021.TorqueConverterPump':
        '''TorqueConverterPump: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'TorqueConverterPump':
            raise CastException('Failed to cast component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2021.TorqueConverterPump)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_torque_converter_turbine(self) -> '_2022.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'TorqueConverterTurbine':
            raise CastException('Failed to cast component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2022.TorqueConverterTurbine)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cvt_pulley(self) -> '_2023.CVTPulley':
        '''CVTPulley: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'CVTPulley':
            raise CastException('Failed to cast component to CVTPulley. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2023.CVTPulley)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_half(self) -> '_2024.SynchroniserHalf':
        '''SynchroniserHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'SynchroniserHalf':
            raise CastException('Failed to cast component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2024.SynchroniserHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_sleeve(self) -> '_2025.SynchroniserSleeve':
        '''SynchroniserSleeve: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Component.__class__.__qualname__ != 'SynchroniserSleeve':
            raise CastException('Failed to cast component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2025.SynchroniserSleeve)(self.wrapped.Component) if self.wrapped.Component else None
