'''_2944.py

PartSteadyStateSynchronousResponseOnAShaft
'''


from mastapy.system_model.part_model import (
    _1931, _1904, _1935, _1911,
    _1920, _1910, _1916, _1919,
    _1921, _1924, _1932, _1908,
    _1929, _1926, _1927, _1933,
    _1934, _1938
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.couplings import (
    _1974, _1976, _1977, _1995,
    _1996, _1997, _1998, _1999,
    _2002, _2024, _2025, _2026,
    _2027, _2028, _2030, _2031,
    _2032, _2033, _2034
)
from mastapy.system_model.part_model.gears import (
    _1978, _1980, _1981, _1982,
    _1986, _1987, _1988, _1989,
    _1990, _1991, _1992, _1993,
    _1994, _2003, _2005, _2006,
    _2007, _2011, _2012, _2013,
    _2014, _2015, _2016, _2017,
    _2018, _2019, _2020, _2021,
    _2022, _2023
)
from mastapy.system_model.part_model.shaft_model import _1942
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import _3084
from mastapy.system_model.analyses_and_results.analysis_cases import _4455
from mastapy._internal.python_net import python_net_import

_PART_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'PartSteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('PartSteadyStateSynchronousResponseOnAShaft',)


class PartSteadyStateSynchronousResponseOnAShaft(_4455.PartStaticLoadAnalysisCase):
    '''PartSteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _PART_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartSteadyStateSynchronousResponseOnAShaft.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1931.Part':
        '''Part: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1931.Part)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_assembly(self) -> '_1904.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Assembly':
            raise CastException('Failed to cast component_design to Assembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1904.Assembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_root_assembly(self) -> '_1935.RootAssembly':
        '''RootAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'RootAssembly':
            raise CastException('Failed to cast component_design to RootAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1935.RootAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bolted_joint(self) -> '_1911.BoltedJoint':
        '''BoltedJoint: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BoltedJoint':
            raise CastException('Failed to cast component_design to BoltedJoint. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1911.BoltedJoint)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_flexible_pin_assembly(self) -> '_1920.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'FlexiblePinAssembly':
            raise CastException('Failed to cast component_design to FlexiblePinAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1920.FlexiblePinAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_belt_drive(self) -> '_1974.BeltDrive':
        '''BeltDrive: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BeltDrive':
            raise CastException('Failed to cast component_design to BeltDrive. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1974.BeltDrive)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring_assembly(self) -> '_1976.RollingRingAssembly':
        '''RollingRingAssembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'RollingRingAssembly':
            raise CastException('Failed to cast component_design to RollingRingAssembly. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1976.RollingRingAssembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser(self) -> '_1977.Synchroniser':
        '''Synchroniser: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Synchroniser':
            raise CastException('Failed to cast component_design to Synchroniser. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1977.Synchroniser)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear_set(self) -> '_1978.ConceptGearSet':
        '''ConceptGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ConceptGearSet':
            raise CastException('Failed to cast component_design to ConceptGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1978.ConceptGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear_set(self) -> '_1980.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CylindricalGearSet':
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1980.CylindricalGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear_set(self) -> '_1981.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'FaceGearSet':
            raise CastException('Failed to cast component_design to FaceGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1981.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear_set(self) -> '_1982.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'WormGearSet':
            raise CastException('Failed to cast component_design to WormGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1982.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear_set(self) -> '_1986.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'HypoidGearSet':
            raise CastException('Failed to cast component_design to HypoidGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1986.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear_set(self) -> '_1987.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialGearSet':
            raise CastException('Failed to cast component_design to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1987.BevelDifferentialGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear_set(self) -> '_1988.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SpiralBevelGearSet':
            raise CastException('Failed to cast component_design to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1988.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear_set(self) -> '_1989.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelDiffGearSet':
            raise CastException('Failed to cast component_design to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1989.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear_set(self) -> '_1990.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelGearSet':
            raise CastException('Failed to cast component_design to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1990.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear_set(self) -> '_1991.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ZerolBevelGearSet':
            raise CastException('Failed to cast component_design to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1991.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_1992.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearSet':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1992.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_1993.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearSet':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1993.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_planetary_gear_set(self) -> '_1994.PlanetaryGearSet':
        '''PlanetaryGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'PlanetaryGearSet':
            raise CastException('Failed to cast component_design to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1994.PlanetaryGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt(self) -> '_1995.CVT':
        '''CVT: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CVT':
            raise CastException('Failed to cast component_design to CVT. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1995.CVT)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch(self) -> '_1996.Clutch':
        '''Clutch: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Clutch':
            raise CastException('Failed to cast component_design to Clutch. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1996.Clutch)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling(self) -> '_1997.ConceptCoupling':
        '''ConceptCoupling: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ConceptCoupling':
            raise CastException('Failed to cast component_design to ConceptCoupling. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1997.ConceptCoupling)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper(self) -> '_1998.SpringDamper':
        '''SpringDamper: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SpringDamper':
            raise CastException('Failed to cast component_design to SpringDamper. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1998.SpringDamper)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter(self) -> '_1999.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'TorqueConverter':
            raise CastException('Failed to cast component_design to TorqueConverter. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1999.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bolt(self) -> '_1910.Bolt':
        '''Bolt: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Bolt':
            raise CastException('Failed to cast component_design to Bolt. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1910.Bolt)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_datum(self) -> '_1916.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Datum':
            raise CastException('Failed to cast component_design to Datum. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1916.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_external_cad_model(self) -> '_1919.ExternalCADModel':
        '''ExternalCADModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ExternalCADModel':
            raise CastException('Failed to cast component_design to ExternalCADModel. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1919.ExternalCADModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_guide_dxf_model(self) -> '_1921.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'GuideDxfModel':
            raise CastException('Failed to cast component_design to GuideDxfModel. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1921.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_imported_fe_component(self) -> '_1924.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ImportedFEComponent':
            raise CastException('Failed to cast component_design to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1924.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_1942.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Shaft':
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1942.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_planet_carrier(self) -> '_1932.PlanetCarrier':
        '''PlanetCarrier: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'PlanetCarrier':
            raise CastException('Failed to cast component_design to PlanetCarrier. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1932.PlanetCarrier)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bearing(self) -> '_1908.Bearing':
        '''Bearing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Bearing':
            raise CastException('Failed to cast component_design to Bearing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1908.Bearing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_oil_seal(self) -> '_1929.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'OilSeal':
            raise CastException('Failed to cast component_design to OilSeal. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1929.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft_hub_connection(self) -> '_2002.ShaftHubConnection':
        '''ShaftHubConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ShaftHubConnection':
            raise CastException('Failed to cast component_design to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2002.ShaftHubConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_mass_disc(self) -> '_1926.MassDisc':
        '''MassDisc: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'MassDisc':
            raise CastException('Failed to cast component_design to MassDisc. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1926.MassDisc)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_measurement_component(self) -> '_1927.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'MeasurementComponent':
            raise CastException('Failed to cast component_design to MeasurementComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1927.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_point_load(self) -> '_1933.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'PointLoad':
            raise CastException('Failed to cast component_design to PointLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1933.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_power_load(self) -> '_1934.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'PowerLoad':
            raise CastException('Failed to cast component_design to PowerLoad. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1934.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_unbalanced_mass(self) -> '_1938.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'UnbalancedMass':
            raise CastException('Failed to cast component_design to UnbalancedMass. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1938.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear(self) -> '_2003.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ConceptGear':
            raise CastException('Failed to cast component_design to ConceptGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2003.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear(self) -> '_2005.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CylindricalGear':
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2005.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear(self) -> '_2006.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'FaceGear':
            raise CastException('Failed to cast component_design to FaceGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2006.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear(self) -> '_2007.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'WormGear':
            raise CastException('Failed to cast component_design to WormGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2007.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear(self) -> '_2011.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'HypoidGear':
            raise CastException('Failed to cast component_design to HypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2011.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear(self) -> '_2012.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialGear':
            raise CastException('Failed to cast component_design to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2012.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear(self) -> '_2013.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SpiralBevelGear':
            raise CastException('Failed to cast component_design to SpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2013.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear(self) -> '_2014.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelDiffGear':
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2014.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear(self) -> '_2015.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelGear':
            raise CastException('Failed to cast component_design to StraightBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2015.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear(self) -> '_2016.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ZerolBevelGear':
            raise CastException('Failed to cast component_design to ZerolBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2016.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_planet_gear(self) -> '_2017.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialPlanetGear':
            raise CastException('Failed to cast component_design to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2017.BevelDifferentialPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_sun_gear(self) -> '_2018.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialSunGear':
            raise CastException('Failed to cast component_design to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2018.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_planet_gear(self) -> '_2019.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelPlanetGear':
            raise CastException('Failed to cast component_design to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2019.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_sun_gear(self) -> '_2020.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelSunGear':
            raise CastException('Failed to cast component_design to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2020.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2021.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGear':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2021.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2022.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGear':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2022.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_planet_gear(self) -> '_2023.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CylindricalPlanetGear':
            raise CastException('Failed to cast component_design to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2023.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch_half(self) -> '_2024.ClutchHalf':
        '''ClutchHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ClutchHalf':
            raise CastException('Failed to cast component_design to ClutchHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2024.ClutchHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling_half(self) -> '_2025.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ConceptCouplingHalf':
            raise CastException('Failed to cast component_design to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2025.ConceptCouplingHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_pulley(self) -> '_2026.Pulley':
        '''Pulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'Pulley':
            raise CastException('Failed to cast component_design to Pulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2026.Pulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring(self) -> '_2027.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'RollingRing':
            raise CastException('Failed to cast component_design to RollingRing. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2027.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper_half(self) -> '_2028.SpringDamperHalf':
        '''SpringDamperHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SpringDamperHalf':
            raise CastException('Failed to cast component_design to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2028.SpringDamperHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_pump(self) -> '_2030.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'TorqueConverterPump':
            raise CastException('Failed to cast component_design to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2030.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_turbine(self) -> '_2031.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'TorqueConverterTurbine':
            raise CastException('Failed to cast component_design to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2031.TorqueConverterTurbine)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt_pulley(self) -> '_2032.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CVTPulley':
            raise CastException('Failed to cast component_design to CVTPulley. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2032.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_half(self) -> '_2033.SynchroniserHalf':
        '''SynchroniserHalf: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SynchroniserHalf':
            raise CastException('Failed to cast component_design to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2033.SynchroniserHalf)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_synchroniser_sleeve(self) -> '_2034.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SynchroniserSleeve':
            raise CastException('Failed to cast component_design to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2034.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def steady_state_synchronous_response_on_a_shaft(self) -> '_3084.SteadyStateSynchronousResponseOnAShaft':
        '''SteadyStateSynchronousResponseOnAShaft: 'SteadyStateSynchronousResponseOnAShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3084.SteadyStateSynchronousResponseOnAShaft)(self.wrapped.SteadyStateSynchronousResponseOnAShaft) if self.wrapped.SteadyStateSynchronousResponseOnAShaft else None
