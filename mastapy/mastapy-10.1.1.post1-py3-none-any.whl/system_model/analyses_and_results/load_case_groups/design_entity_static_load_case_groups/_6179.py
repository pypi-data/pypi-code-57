'''_6179.py

PartStaticLoadCaseGroup
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _1931, _1904, _1935, _1911,
    _1920, _1910, _1916, _1919,
    _1921, _1924, _1932, _1908,
    _1929, _1926, _1927, _1933,
    _1934, _1938
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.couplings import (
    _1973, _1975, _1976, _1987,
    _1988, _1989, _1990, _1991,
    _1967, _2015, _2016, _2017,
    _2018, _2019, _2021, _2022,
    _2023, _2024, _2025
)
from mastapy.system_model.part_model.gears import (
    _1977, _1968, _1978, _1970,
    _1965, _1981, _1966, _1982,
    _1964, _1983, _1984, _1985,
    _1986, _1994, _1996, _1997,
    _1998, _2002, _2003, _2004,
    _2005, _2006, _2007, _2008,
    _2009, _2010, _2011, _2012,
    _2013, _2014
)
from mastapy.system_model.part_model.shaft_model import _1942
from mastapy.system_model.analyses_and_results.static_loads import _2291
from mastapy.system_model.analyses_and_results.load_case_groups.design_entity_static_load_case_groups import _6177
from mastapy._internal.python_net import python_net_import

_PART_STATIC_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups.DesignEntityStaticLoadCaseGroups', 'PartStaticLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('PartStaticLoadCaseGroup',)


class PartStaticLoadCaseGroup(_6177.DesignEntityStaticLoadCaseGroup):
    '''PartStaticLoadCaseGroup

    This is a mastapy class.
    '''

    TYPE = _PART_STATIC_LOAD_CASE_GROUP
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartStaticLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def clear_user_specified_excitation_data_for_all_load_cases(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'ClearUserSpecifiedExcitationDataForAllLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ClearUserSpecifiedExcitationDataForAllLoadCases

    @property
    def part(self) -> '_1931.Part':
        '''Part: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1931.Part)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_assembly(self) -> '_1904.Assembly':
        '''Assembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'Assembly':
            raise CastException('Failed to cast part to Assembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1904.Assembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_root_assembly(self) -> '_1935.RootAssembly':
        '''RootAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'RootAssembly':
            raise CastException('Failed to cast part to RootAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1935.RootAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bolted_joint(self) -> '_1911.BoltedJoint':
        '''BoltedJoint: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'BoltedJoint':
            raise CastException('Failed to cast part to BoltedJoint. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1911.BoltedJoint)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_flexible_pin_assembly(self) -> '_1920.FlexiblePinAssembly':
        '''FlexiblePinAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'FlexiblePinAssembly':
            raise CastException('Failed to cast part to FlexiblePinAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1920.FlexiblePinAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_belt_drive(self) -> '_1973.BeltDrive':
        '''BeltDrive: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'BeltDrive':
            raise CastException('Failed to cast part to BeltDrive. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1973.BeltDrive)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_rolling_ring_assembly(self) -> '_1975.RollingRingAssembly':
        '''RollingRingAssembly: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'RollingRingAssembly':
            raise CastException('Failed to cast part to RollingRingAssembly. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1975.RollingRingAssembly)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser(self) -> '_1976.Synchroniser':
        '''Synchroniser: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'Synchroniser':
            raise CastException('Failed to cast part to Synchroniser. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1976.Synchroniser)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_gear_set(self) -> '_1977.ConceptGearSet':
        '''ConceptGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'ConceptGearSet':
            raise CastException('Failed to cast part to ConceptGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1977.ConceptGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cylindrical_gear_set(self) -> '_1968.CylindricalGearSet':
        '''CylindricalGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'CylindricalGearSet':
            raise CastException('Failed to cast part to CylindricalGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1968.CylindricalGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_face_gear_set(self) -> '_1978.FaceGearSet':
        '''FaceGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'FaceGearSet':
            raise CastException('Failed to cast part to FaceGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1978.FaceGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_worm_gear_set(self) -> '_1970.WormGearSet':
        '''WormGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'WormGearSet':
            raise CastException('Failed to cast part to WormGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1970.WormGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_hypoid_gear_set(self) -> '_1965.HypoidGearSet':
        '''HypoidGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'HypoidGearSet':
            raise CastException('Failed to cast part to HypoidGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1965.HypoidGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_gear_set(self) -> '_1981.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'BevelDifferentialGearSet':
            raise CastException('Failed to cast part to BevelDifferentialGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1981.BevelDifferentialGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spiral_bevel_gear_set(self) -> '_1966.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'SpiralBevelGearSet':
            raise CastException('Failed to cast part to SpiralBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1966.SpiralBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_diff_gear_set(self) -> '_1982.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'StraightBevelDiffGearSet':
            raise CastException('Failed to cast part to StraightBevelDiffGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1982.StraightBevelDiffGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_gear_set(self) -> '_1964.StraightBevelGearSet':
        '''StraightBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'StraightBevelGearSet':
            raise CastException('Failed to cast part to StraightBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1964.StraightBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_zerol_bevel_gear_set(self) -> '_1983.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'ZerolBevelGearSet':
            raise CastException('Failed to cast part to ZerolBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1983.ZerolBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGearSet':
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidHypoidGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGearSet':
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidSpiralBevelGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1985.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_planetary_gear_set(self) -> '_1986.PlanetaryGearSet':
        '''PlanetaryGearSet: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'PlanetaryGearSet':
            raise CastException('Failed to cast part to PlanetaryGearSet. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1986.PlanetaryGearSet)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cvt(self) -> '_1987.CVT':
        '''CVT: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'CVT':
            raise CastException('Failed to cast part to CVT. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1987.CVT)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_clutch(self) -> '_1988.Clutch':
        '''Clutch: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'Clutch':
            raise CastException('Failed to cast part to Clutch. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1988.Clutch)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_coupling(self) -> '_1989.ConceptCoupling':
        '''ConceptCoupling: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'ConceptCoupling':
            raise CastException('Failed to cast part to ConceptCoupling. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1989.ConceptCoupling)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spring_damper(self) -> '_1990.SpringDamper':
        '''SpringDamper: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'SpringDamper':
            raise CastException('Failed to cast part to SpringDamper. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1990.SpringDamper)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_torque_converter(self) -> '_1991.TorqueConverter':
        '''TorqueConverter: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'TorqueConverter':
            raise CastException('Failed to cast part to TorqueConverter. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1991.TorqueConverter)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bolt(self) -> '_1910.Bolt':
        '''Bolt: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'Bolt':
            raise CastException('Failed to cast part to Bolt. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1910.Bolt)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_datum(self) -> '_1916.Datum':
        '''Datum: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'Datum':
            raise CastException('Failed to cast part to Datum. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1916.Datum)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_external_cad_model(self) -> '_1919.ExternalCADModel':
        '''ExternalCADModel: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'ExternalCADModel':
            raise CastException('Failed to cast part to ExternalCADModel. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1919.ExternalCADModel)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_guide_dxf_model(self) -> '_1921.GuideDxfModel':
        '''GuideDxfModel: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'GuideDxfModel':
            raise CastException('Failed to cast part to GuideDxfModel. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1921.GuideDxfModel)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_imported_fe_component(self) -> '_1924.ImportedFEComponent':
        '''ImportedFEComponent: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'ImportedFEComponent':
            raise CastException('Failed to cast part to ImportedFEComponent. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1924.ImportedFEComponent)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_shaft(self) -> '_1942.Shaft':
        '''Shaft: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'Shaft':
            raise CastException('Failed to cast part to Shaft. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1942.Shaft)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_planet_carrier(self) -> '_1932.PlanetCarrier':
        '''PlanetCarrier: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'PlanetCarrier':
            raise CastException('Failed to cast part to PlanetCarrier. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1932.PlanetCarrier)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bearing(self) -> '_1908.Bearing':
        '''Bearing: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'Bearing':
            raise CastException('Failed to cast part to Bearing. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1908.Bearing)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_oil_seal(self) -> '_1929.OilSeal':
        '''OilSeal: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'OilSeal':
            raise CastException('Failed to cast part to OilSeal. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1929.OilSeal)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_shaft_hub_connection(self) -> '_1967.ShaftHubConnection':
        '''ShaftHubConnection: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'ShaftHubConnection':
            raise CastException('Failed to cast part to ShaftHubConnection. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1967.ShaftHubConnection)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_mass_disc(self) -> '_1926.MassDisc':
        '''MassDisc: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'MassDisc':
            raise CastException('Failed to cast part to MassDisc. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1926.MassDisc)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_measurement_component(self) -> '_1927.MeasurementComponent':
        '''MeasurementComponent: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'MeasurementComponent':
            raise CastException('Failed to cast part to MeasurementComponent. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1927.MeasurementComponent)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_point_load(self) -> '_1933.PointLoad':
        '''PointLoad: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'PointLoad':
            raise CastException('Failed to cast part to PointLoad. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1933.PointLoad)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_power_load(self) -> '_1934.PowerLoad':
        '''PowerLoad: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'PowerLoad':
            raise CastException('Failed to cast part to PowerLoad. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1934.PowerLoad)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_unbalanced_mass(self) -> '_1938.UnbalancedMass':
        '''UnbalancedMass: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'UnbalancedMass':
            raise CastException('Failed to cast part to UnbalancedMass. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1938.UnbalancedMass)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_gear(self) -> '_1994.ConceptGear':
        '''ConceptGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'ConceptGear':
            raise CastException('Failed to cast part to ConceptGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1994.ConceptGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cylindrical_gear(self) -> '_1996.CylindricalGear':
        '''CylindricalGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'CylindricalGear':
            raise CastException('Failed to cast part to CylindricalGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1996.CylindricalGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_face_gear(self) -> '_1997.FaceGear':
        '''FaceGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'FaceGear':
            raise CastException('Failed to cast part to FaceGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1997.FaceGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_worm_gear(self) -> '_1998.WormGear':
        '''WormGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'WormGear':
            raise CastException('Failed to cast part to WormGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_1998.WormGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_hypoid_gear(self) -> '_2002.HypoidGear':
        '''HypoidGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'HypoidGear':
            raise CastException('Failed to cast part to HypoidGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2002.HypoidGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_gear(self) -> '_2003.BevelDifferentialGear':
        '''BevelDifferentialGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'BevelDifferentialGear':
            raise CastException('Failed to cast part to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2003.BevelDifferentialGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spiral_bevel_gear(self) -> '_2004.SpiralBevelGear':
        '''SpiralBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'SpiralBevelGear':
            raise CastException('Failed to cast part to SpiralBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2004.SpiralBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_diff_gear(self) -> '_2005.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'StraightBevelDiffGear':
            raise CastException('Failed to cast part to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2005.StraightBevelDiffGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_gear(self) -> '_2006.StraightBevelGear':
        '''StraightBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'StraightBevelGear':
            raise CastException('Failed to cast part to StraightBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2006.StraightBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_zerol_bevel_gear(self) -> '_2007.ZerolBevelGear':
        '''ZerolBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'ZerolBevelGear':
            raise CastException('Failed to cast part to ZerolBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2007.ZerolBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_planet_gear(self) -> '_2008.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'BevelDifferentialPlanetGear':
            raise CastException('Failed to cast part to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2008.BevelDifferentialPlanetGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_bevel_differential_sun_gear(self) -> '_2009.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'BevelDifferentialSunGear':
            raise CastException('Failed to cast part to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2009.BevelDifferentialSunGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_planet_gear(self) -> '_2010.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'StraightBevelPlanetGear':
            raise CastException('Failed to cast part to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2010.StraightBevelPlanetGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_straight_bevel_sun_gear(self) -> '_2011.StraightBevelSunGear':
        '''StraightBevelSunGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'StraightBevelSunGear':
            raise CastException('Failed to cast part to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2011.StraightBevelSunGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2012.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGear':
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2012.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2013.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGear':
            raise CastException('Failed to cast part to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2013.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cylindrical_planet_gear(self) -> '_2014.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'CylindricalPlanetGear':
            raise CastException('Failed to cast part to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2014.CylindricalPlanetGear)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_clutch_half(self) -> '_2015.ClutchHalf':
        '''ClutchHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'ClutchHalf':
            raise CastException('Failed to cast part to ClutchHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2015.ClutchHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_concept_coupling_half(self) -> '_2016.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'ConceptCouplingHalf':
            raise CastException('Failed to cast part to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2016.ConceptCouplingHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_pulley(self) -> '_2017.Pulley':
        '''Pulley: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'Pulley':
            raise CastException('Failed to cast part to Pulley. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2017.Pulley)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_rolling_ring(self) -> '_2018.RollingRing':
        '''RollingRing: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'RollingRing':
            raise CastException('Failed to cast part to RollingRing. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2018.RollingRing)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_spring_damper_half(self) -> '_2019.SpringDamperHalf':
        '''SpringDamperHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'SpringDamperHalf':
            raise CastException('Failed to cast part to SpringDamperHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2019.SpringDamperHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_torque_converter_pump(self) -> '_2021.TorqueConverterPump':
        '''TorqueConverterPump: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'TorqueConverterPump':
            raise CastException('Failed to cast part to TorqueConverterPump. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2021.TorqueConverterPump)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_torque_converter_turbine(self) -> '_2022.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'TorqueConverterTurbine':
            raise CastException('Failed to cast part to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2022.TorqueConverterTurbine)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_cvt_pulley(self) -> '_2023.CVTPulley':
        '''CVTPulley: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'CVTPulley':
            raise CastException('Failed to cast part to CVTPulley. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2023.CVTPulley)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser_half(self) -> '_2024.SynchroniserHalf':
        '''SynchroniserHalf: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'SynchroniserHalf':
            raise CastException('Failed to cast part to SynchroniserHalf. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2024.SynchroniserHalf)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_of_type_synchroniser_sleeve(self) -> '_2025.SynchroniserSleeve':
        '''SynchroniserSleeve: 'Part' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Part.__class__.__qualname__ != 'SynchroniserSleeve':
            raise CastException('Failed to cast part to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.Part.__class__.__qualname__))

        return constructor.new(_2025.SynchroniserSleeve)(self.wrapped.Part) if self.wrapped.Part else None

    @property
    def part_load_cases(self) -> 'List[_2291.PartLoadCase]':
        '''List[PartLoadCase]: 'PartLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartLoadCases, constructor.new(_2291.PartLoadCase))
        return value
