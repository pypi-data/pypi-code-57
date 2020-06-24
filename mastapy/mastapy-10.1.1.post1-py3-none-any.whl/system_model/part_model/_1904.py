'''_1904.py

Assembly
'''


from typing import List, TypeVar, Optional

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import list_with_selected_item
from mastapy.system_model.part_model import (
    _1916, _1912, _1908, _1911,
    _1924, _1934, _1933, _1929,
    _1931, _1905, _1937, _1935,
    _1920, _1906, _1910, _1919,
    _1921, _1928, _1915, _1932,
    _1939, _1926, _1927, _1938
)
from mastapy.system_model.part_model.gears import (
    _1964, _1965, _1966, _1968,
    _1969, _1970, _1971, _1972,
    _1977, _1978, _1979, _1980,
    _1981, _1982, _1983, _1984,
    _1985, _1986, _1992, _1994,
    _1995, _1996, _1997, _1998,
    _1999, _2000, _2001, _2002,
    _2003, _2004, _2005, _2006,
    _2007, _2008, _2009, _2010,
    _2011, _2012, _2013, _2014
)
from mastapy.system_model.part_model.couplings import (
    _1967, _1973, _1974, _1975,
    _1976, _1987, _1988, _1989,
    _1990, _1991, _1993, _2015,
    _2016, _2017, _2018, _2019,
    _2020, _2021, _2022, _2023,
    _2024, _2025
)
from mastapy.system_model.part_model.shaft_model import _1942
from mastapy.system_model.part_model.creation_options import (
    _2026, _2027, _2028, _2029
)
from mastapy.gears.gear_designs.creation_options import _1066, _1069
from mastapy.gears import _305
from mastapy.nodal_analysis import _109
from mastapy.bearings import _1460, _1484
from mastapy._internal.python_net import python_net_import

_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')


__docformat__ = 'restructuredtext en'
__all__ = ('Assembly',)


class Assembly(_1905.AbstractAssembly):
    '''Assembly

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'Assembly.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def face_width_of_widest_cylindrical_gear(self) -> 'float':
        '''float: 'FaceWidthOfWidestCylindricalGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FaceWidthOfWidestCylindricalGear

    @property
    def mass_of_gears(self) -> 'float':
        '''float: 'MassOfGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfGears

    @property
    def mass_of_bearings(self) -> 'float':
        '''float: 'MassOfBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfBearings

    @property
    def mass_of_shafts(self) -> 'float':
        '''float: 'MassOfShafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfShafts

    @property
    def mass_of_imported_fe_shafts(self) -> 'float':
        '''float: 'MassOfImportedFEShafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfImportedFEShafts

    @property
    def mass_of_imported_fe_housings(self) -> 'float':
        '''float: 'MassOfImportedFEHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfImportedFEHousings

    @property
    def mass_of_other_parts(self) -> 'float':
        '''float: 'MassOfOtherParts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassOfOtherParts

    @property
    def oil_level_specified(self) -> 'bool':
        '''bool: 'OilLevelSpecified' is the original name of this property.'''

        return self.wrapped.OilLevelSpecified

    @oil_level_specified.setter
    def oil_level_specified(self, value: 'bool'):
        self.wrapped.OilLevelSpecified = bool(value) if value else False

    @property
    def oil_level_reference_datum(self) -> 'list_with_selected_item.ListWithSelectedItem_Datum':
        '''list_with_selected_item.ListWithSelectedItem_Datum: 'OilLevelReferenceDatum' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_Datum)(self.wrapped.OilLevelReferenceDatum) if self.wrapped.OilLevelReferenceDatum else None

    @oil_level_reference_datum.setter
    def oil_level_reference_datum(self, value: 'list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_Datum.TYPE
        enclosed_type = list_with_selected_item.ListWithSelectedItem_Datum.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.OilLevelReferenceDatum = value

    @property
    def oil_level(self) -> 'float':
        '''float: 'OilLevel' is the original name of this property.'''

        return self.wrapped.OilLevel

    @oil_level.setter
    def oil_level(self, value: 'float'):
        self.wrapped.OilLevel = float(value) if value else 0.0

    @property
    def smallest_number_of_teeth(self) -> 'int':
        '''int: 'SmallestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SmallestNumberOfTeeth

    @property
    def largest_number_of_teeth(self) -> 'int':
        '''int: 'LargestNumberOfTeeth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LargestNumberOfTeeth

    @property
    def transverse_and_axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseAndAxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseAndAxialContactRatioRatingForNVH

    @property
    def transverse_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseContactRatioRatingForNVH

    @property
    def axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'AxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialContactRatioRatingForNVH

    @property
    def minimum_tip_thickness(self) -> 'float':
        '''float: 'MinimumTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumTipThickness

    @property
    def components_with_unknown_scalar_mass(self) -> 'List[_1912.Component]':
        '''List[Component]: 'ComponentsWithUnknownScalarMass' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentsWithUnknownScalarMass, constructor.new(_1912.Component))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_1964.StraightBevelGearSet]':
        '''List[StraightBevelGearSet]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_1964.StraightBevelGearSet))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_1965.HypoidGearSet]':
        '''List[HypoidGearSet]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_1965.HypoidGearSet))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_1966.SpiralBevelGearSet]':
        '''List[SpiralBevelGearSet]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_1966.SpiralBevelGearSet))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_1967.ShaftHubConnection]':
        '''List[ShaftHubConnection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_1967.ShaftHubConnection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_1968.CylindricalGearSet]':
        '''List[CylindricalGearSet]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_1968.CylindricalGearSet))
        return value

    @property
    def conical_gear_sets(self) -> 'List[_1969.ConicalGearSet]':
        '''List[ConicalGearSet]: 'ConicalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConicalGearSets, constructor.new(_1969.ConicalGearSet))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_1970.WormGearSet]':
        '''List[WormGearSet]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_1970.WormGearSet))
        return value

    @property
    def klingelnberg_cyclo_palloid_gear_sets(self) -> 'List[_1971.KlingelnbergCycloPalloidConicalGearSet]':
        '''List[KlingelnbergCycloPalloidConicalGearSet]: 'KlingelnbergCycloPalloidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidGearSets, constructor.new(_1971.KlingelnbergCycloPalloidConicalGearSet))
        return value

    @property
    def shafts(self) -> 'List[_1942.Shaft]':
        '''List[Shaft]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_1942.Shaft))
        return value

    @property
    def bearings(self) -> 'List[_1908.Bearing]':
        '''List[Bearing]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_1908.Bearing))
        return value

    @property
    def bolted_joints(self) -> 'List[_1911.BoltedJoint]':
        '''List[BoltedJoint]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_1911.BoltedJoint))
        return value

    @property
    def imported_fes(self) -> 'List[_1924.ImportedFEComponent]':
        '''List[ImportedFEComponent]: 'ImportedFEs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEs, constructor.new(_1924.ImportedFEComponent))
        return value

    @property
    def component_details(self) -> 'List[_1912.Component]':
        '''List[Component]: 'ComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDetails, constructor.new(_1912.Component))
        return value

    @property
    def power_loads(self) -> 'List[_1934.PowerLoad]':
        '''List[PowerLoad]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_1934.PowerLoad))
        return value

    @property
    def point_loads(self) -> 'List[_1933.PointLoad]':
        '''List[PointLoad]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_1933.PointLoad))
        return value

    @property
    def oil_seals(self) -> 'List[_1929.OilSeal]':
        '''List[OilSeal]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_1929.OilSeal))
        return value

    def get_part_named_of_type_abstract_assembly(self, name: 'str') -> '_1905.AbstractAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.AbstractAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1905.AbstractAssembly.TYPE](name if name else None)
        return constructor.new(_1905.AbstractAssembly)(method_result) if method_result else None

    def get_part_named_of_type_component(self, name: 'str') -> '_1912.Component':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Component
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1912.Component.TYPE](name if name else None)
        return constructor.new(_1912.Component)(method_result) if method_result else None

    def get_part_named_of_type_assembly(self, name: 'str') -> 'Assembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Assembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[Assembly.TYPE](name if name else None)
        return constructor.new(Assembly)(method_result) if method_result else None

    def get_part_named_of_type_specialised_assembly(self, name: 'str') -> '_1937.SpecialisedAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.SpecialisedAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1937.SpecialisedAssembly.TYPE](name if name else None)
        return constructor.new(_1937.SpecialisedAssembly)(method_result) if method_result else None

    def get_part_named_of_type_root_assembly(self, name: 'str') -> '_1935.RootAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.RootAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1935.RootAssembly.TYPE](name if name else None)
        return constructor.new(_1935.RootAssembly)(method_result) if method_result else None

    def get_part_named_of_type_bolted_joint(self, name: 'str') -> '_1911.BoltedJoint':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.BoltedJoint
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1911.BoltedJoint.TYPE](name if name else None)
        return constructor.new(_1911.BoltedJoint)(method_result) if method_result else None

    def get_part_named_of_type_flexible_pin_assembly(self, name: 'str') -> '_1920.FlexiblePinAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.FlexiblePinAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1920.FlexiblePinAssembly.TYPE](name if name else None)
        return constructor.new(_1920.FlexiblePinAssembly)(method_result) if method_result else None

    def get_part_named_of_type_gear_set(self, name: 'str') -> '_1972.GearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.GearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1972.GearSet.TYPE](name if name else None)
        return constructor.new(_1972.GearSet)(method_result) if method_result else None

    def get_part_named_of_type_belt_drive(self, name: 'str') -> '_1973.BeltDrive':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1973.BeltDrive.TYPE](name if name else None)
        return constructor.new(_1973.BeltDrive)(method_result) if method_result else None

    def get_part_named_of_type_coupling(self, name: 'str') -> '_1974.Coupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Coupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1974.Coupling.TYPE](name if name else None)
        return constructor.new(_1974.Coupling)(method_result) if method_result else None

    def get_part_named_of_type_rolling_ring_assembly(self, name: 'str') -> '_1975.RollingRingAssembly':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRingAssembly
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1975.RollingRingAssembly.TYPE](name if name else None)
        return constructor.new(_1975.RollingRingAssembly)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser(self, name: 'str') -> '_1976.Synchroniser':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Synchroniser
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1976.Synchroniser.TYPE](name if name else None)
        return constructor.new(_1976.Synchroniser)(method_result) if method_result else None

    def get_part_named_of_type_concept_gear_set(self, name: 'str') -> '_1977.ConceptGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConceptGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1977.ConceptGearSet.TYPE](name if name else None)
        return constructor.new(_1977.ConceptGearSet)(method_result) if method_result else None

    def get_part_named_of_type_conical_gear_set(self, name: 'str') -> '_1969.ConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1969.ConicalGearSet.TYPE](name if name else None)
        return constructor.new(_1969.ConicalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_gear_set(self, name: 'str') -> '_1968.CylindricalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1968.CylindricalGearSet.TYPE](name if name else None)
        return constructor.new(_1968.CylindricalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_face_gear_set(self, name: 'str') -> '_1978.FaceGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.FaceGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1978.FaceGearSet.TYPE](name if name else None)
        return constructor.new(_1978.FaceGearSet)(method_result) if method_result else None

    def get_part_named_of_type_worm_gear_set(self, name: 'str') -> '_1970.WormGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.WormGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1970.WormGearSet.TYPE](name if name else None)
        return constructor.new(_1970.WormGearSet)(method_result) if method_result else None

    def get_part_named_of_type_agma_gleason_conical_gear_set(self, name: 'str') -> '_1979.AGMAGleasonConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1979.AGMAGleasonConicalGearSet.TYPE](name if name else None)
        return constructor.new(_1979.AGMAGleasonConicalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self, name: 'str') -> '_1971.KlingelnbergCycloPalloidConicalGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1971.KlingelnbergCycloPalloidConicalGearSet.TYPE](name if name else None)
        return constructor.new(_1971.KlingelnbergCycloPalloidConicalGearSet)(method_result) if method_result else None

    def get_part_named_of_type_bevel_gear_set(self, name: 'str') -> '_1980.BevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1980.BevelGearSet.TYPE](name if name else None)
        return constructor.new(_1980.BevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_hypoid_gear_set(self, name: 'str') -> '_1965.HypoidGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1965.HypoidGearSet.TYPE](name if name else None)
        return constructor.new(_1965.HypoidGearSet)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_gear_set(self, name: 'str') -> '_1981.BevelDifferentialGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1981.BevelDifferentialGearSet.TYPE](name if name else None)
        return constructor.new(_1981.BevelDifferentialGearSet)(method_result) if method_result else None

    def get_part_named_of_type_spiral_bevel_gear_set(self, name: 'str') -> '_1966.SpiralBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1966.SpiralBevelGearSet.TYPE](name if name else None)
        return constructor.new(_1966.SpiralBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_diff_gear_set(self, name: 'str') -> '_1982.StraightBevelDiffGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1982.StraightBevelDiffGearSet.TYPE](name if name else None)
        return constructor.new(_1982.StraightBevelDiffGearSet)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_gear_set(self, name: 'str') -> '_1964.StraightBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1964.StraightBevelGearSet.TYPE](name if name else None)
        return constructor.new(_1964.StraightBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_zerol_bevel_gear_set(self, name: 'str') -> '_1983.ZerolBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1983.ZerolBevelGearSet.TYPE](name if name else None)
        return constructor.new(_1983.ZerolBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self, name: 'str') -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1984.KlingelnbergCycloPalloidHypoidGearSet.TYPE](name if name else None)
        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, name: 'str') -> '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1985.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE](name if name else None)
        return constructor.new(_1985.KlingelnbergCycloPalloidSpiralBevelGearSet)(method_result) if method_result else None

    def get_part_named_of_type_planetary_gear_set(self, name: 'str') -> '_1986.PlanetaryGearSet':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.PlanetaryGearSet
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1986.PlanetaryGearSet.TYPE](name if name else None)
        return constructor.new(_1986.PlanetaryGearSet)(method_result) if method_result else None

    def get_part_named_of_type_cvt(self, name: 'str') -> '_1987.CVT':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CVT
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1987.CVT.TYPE](name if name else None)
        return constructor.new(_1987.CVT)(method_result) if method_result else None

    def get_part_named_of_type_clutch(self, name: 'str') -> '_1988.Clutch':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Clutch
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1988.Clutch.TYPE](name if name else None)
        return constructor.new(_1988.Clutch)(method_result) if method_result else None

    def get_part_named_of_type_concept_coupling(self, name: 'str') -> '_1989.ConceptCoupling':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCoupling
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1989.ConceptCoupling.TYPE](name if name else None)
        return constructor.new(_1989.ConceptCoupling)(method_result) if method_result else None

    def get_part_named_of_type_spring_damper(self, name: 'str') -> '_1990.SpringDamper':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamper
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1990.SpringDamper.TYPE](name if name else None)
        return constructor.new(_1990.SpringDamper)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter(self, name: 'str') -> '_1991.TorqueConverter':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverter
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1991.TorqueConverter.TYPE](name if name else None)
        return constructor.new(_1991.TorqueConverter)(method_result) if method_result else None

    def get_part_named_of_type_abstract_shaft_or_housing(self, name: 'str') -> '_1906.AbstractShaftOrHousing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.AbstractShaftOrHousing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1906.AbstractShaftOrHousing.TYPE](name if name else None)
        return constructor.new(_1906.AbstractShaftOrHousing)(method_result) if method_result else None

    def get_part_named_of_type_bolt(self, name: 'str') -> '_1910.Bolt':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bolt
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1910.Bolt.TYPE](name if name else None)
        return constructor.new(_1910.Bolt)(method_result) if method_result else None

    def get_part_named_of_type_datum(self, name: 'str') -> '_1916.Datum':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Datum
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1916.Datum.TYPE](name if name else None)
        return constructor.new(_1916.Datum)(method_result) if method_result else None

    def get_part_named_of_type_external_cad_model(self, name: 'str') -> '_1919.ExternalCADModel':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.ExternalCADModel
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1919.ExternalCADModel.TYPE](name if name else None)
        return constructor.new(_1919.ExternalCADModel)(method_result) if method_result else None

    def get_part_named_of_type_guide_dxf_model(self, name: 'str') -> '_1921.GuideDxfModel':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.GuideDxfModel
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1921.GuideDxfModel.TYPE](name if name else None)
        return constructor.new(_1921.GuideDxfModel)(method_result) if method_result else None

    def get_part_named_of_type_mountable_component(self, name: 'str') -> '_1928.MountableComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MountableComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1928.MountableComponent.TYPE](name if name else None)
        return constructor.new(_1928.MountableComponent)(method_result) if method_result else None

    def get_part_named_of_type_imported_fe_component(self, name: 'str') -> '_1924.ImportedFEComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.ImportedFEComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1924.ImportedFEComponent.TYPE](name if name else None)
        return constructor.new(_1924.ImportedFEComponent)(method_result) if method_result else None

    def get_part_named_of_type_shaft(self, name: 'str') -> '_1942.Shaft':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1942.Shaft.TYPE](name if name else None)
        return constructor.new(_1942.Shaft)(method_result) if method_result else None

    def get_part_named_of_type_connector(self, name: 'str') -> '_1915.Connector':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Connector
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1915.Connector.TYPE](name if name else None)
        return constructor.new(_1915.Connector)(method_result) if method_result else None

    def get_part_named_of_type_planet_carrier(self, name: 'str') -> '_1932.PlanetCarrier':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1932.PlanetCarrier.TYPE](name if name else None)
        return constructor.new(_1932.PlanetCarrier)(method_result) if method_result else None

    def get_part_named_of_type_virtual_component(self, name: 'str') -> '_1939.VirtualComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.VirtualComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1939.VirtualComponent.TYPE](name if name else None)
        return constructor.new(_1939.VirtualComponent)(method_result) if method_result else None

    def get_part_named_of_type_gear(self, name: 'str') -> '_1992.Gear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.Gear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1992.Gear.TYPE](name if name else None)
        return constructor.new(_1992.Gear)(method_result) if method_result else None

    def get_part_named_of_type_coupling_half(self, name: 'str') -> '_1993.CouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1993.CouplingHalf.TYPE](name if name else None)
        return constructor.new(_1993.CouplingHalf)(method_result) if method_result else None

    def get_part_named_of_type_bearing(self, name: 'str') -> '_1908.Bearing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1908.Bearing.TYPE](name if name else None)
        return constructor.new(_1908.Bearing)(method_result) if method_result else None

    def get_part_named_of_type_oil_seal(self, name: 'str') -> '_1929.OilSeal':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.OilSeal
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1929.OilSeal.TYPE](name if name else None)
        return constructor.new(_1929.OilSeal)(method_result) if method_result else None

    def get_part_named_of_type_shaft_hub_connection(self, name: 'str') -> '_1967.ShaftHubConnection':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ShaftHubConnection
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1967.ShaftHubConnection.TYPE](name if name else None)
        return constructor.new(_1967.ShaftHubConnection)(method_result) if method_result else None

    def get_part_named_of_type_mass_disc(self, name: 'str') -> '_1926.MassDisc':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MassDisc
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1926.MassDisc.TYPE](name if name else None)
        return constructor.new(_1926.MassDisc)(method_result) if method_result else None

    def get_part_named_of_type_measurement_component(self, name: 'str') -> '_1927.MeasurementComponent':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.MeasurementComponent
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1927.MeasurementComponent.TYPE](name if name else None)
        return constructor.new(_1927.MeasurementComponent)(method_result) if method_result else None

    def get_part_named_of_type_point_load(self, name: 'str') -> '_1933.PointLoad':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PointLoad
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1933.PointLoad.TYPE](name if name else None)
        return constructor.new(_1933.PointLoad)(method_result) if method_result else None

    def get_part_named_of_type_power_load(self, name: 'str') -> '_1934.PowerLoad':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.PowerLoad
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1934.PowerLoad.TYPE](name if name else None)
        return constructor.new(_1934.PowerLoad)(method_result) if method_result else None

    def get_part_named_of_type_unbalanced_mass(self, name: 'str') -> '_1938.UnbalancedMass':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.UnbalancedMass
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1938.UnbalancedMass.TYPE](name if name else None)
        return constructor.new(_1938.UnbalancedMass)(method_result) if method_result else None

    def get_part_named_of_type_concept_gear(self, name: 'str') -> '_1994.ConceptGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConceptGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1994.ConceptGear.TYPE](name if name else None)
        return constructor.new(_1994.ConceptGear)(method_result) if method_result else None

    def get_part_named_of_type_conical_gear(self, name: 'str') -> '_1995.ConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1995.ConicalGear.TYPE](name if name else None)
        return constructor.new(_1995.ConicalGear)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_gear(self, name: 'str') -> '_1996.CylindricalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1996.CylindricalGear.TYPE](name if name else None)
        return constructor.new(_1996.CylindricalGear)(method_result) if method_result else None

    def get_part_named_of_type_face_gear(self, name: 'str') -> '_1997.FaceGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.FaceGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1997.FaceGear.TYPE](name if name else None)
        return constructor.new(_1997.FaceGear)(method_result) if method_result else None

    def get_part_named_of_type_worm_gear(self, name: 'str') -> '_1998.WormGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.WormGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1998.WormGear.TYPE](name if name else None)
        return constructor.new(_1998.WormGear)(method_result) if method_result else None

    def get_part_named_of_type_agma_gleason_conical_gear(self, name: 'str') -> '_1999.AGMAGleasonConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.AGMAGleasonConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_1999.AGMAGleasonConicalGear.TYPE](name if name else None)
        return constructor.new(_1999.AGMAGleasonConicalGear)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_conical_gear(self, name: 'str') -> '_2000.KlingelnbergCycloPalloidConicalGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2000.KlingelnbergCycloPalloidConicalGear.TYPE](name if name else None)
        return constructor.new(_2000.KlingelnbergCycloPalloidConicalGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_gear(self, name: 'str') -> '_2001.BevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2001.BevelGear.TYPE](name if name else None)
        return constructor.new(_2001.BevelGear)(method_result) if method_result else None

    def get_part_named_of_type_hypoid_gear(self, name: 'str') -> '_2002.HypoidGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2002.HypoidGear.TYPE](name if name else None)
        return constructor.new(_2002.HypoidGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_gear(self, name: 'str') -> '_2003.BevelDifferentialGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2003.BevelDifferentialGear.TYPE](name if name else None)
        return constructor.new(_2003.BevelDifferentialGear)(method_result) if method_result else None

    def get_part_named_of_type_spiral_bevel_gear(self, name: 'str') -> '_2004.SpiralBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2004.SpiralBevelGear.TYPE](name if name else None)
        return constructor.new(_2004.SpiralBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_diff_gear(self, name: 'str') -> '_2005.StraightBevelDiffGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2005.StraightBevelDiffGear.TYPE](name if name else None)
        return constructor.new(_2005.StraightBevelDiffGear)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_gear(self, name: 'str') -> '_2006.StraightBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2006.StraightBevelGear.TYPE](name if name else None)
        return constructor.new(_2006.StraightBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_zerol_bevel_gear(self, name: 'str') -> '_2007.ZerolBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2007.ZerolBevelGear.TYPE](name if name else None)
        return constructor.new(_2007.ZerolBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_planet_gear(self, name: 'str') -> '_2008.BevelDifferentialPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2008.BevelDifferentialPlanetGear.TYPE](name if name else None)
        return constructor.new(_2008.BevelDifferentialPlanetGear)(method_result) if method_result else None

    def get_part_named_of_type_bevel_differential_sun_gear(self, name: 'str') -> '_2009.BevelDifferentialSunGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialSunGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2009.BevelDifferentialSunGear.TYPE](name if name else None)
        return constructor.new(_2009.BevelDifferentialSunGear)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_planet_gear(self, name: 'str') -> '_2010.StraightBevelPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2010.StraightBevelPlanetGear.TYPE](name if name else None)
        return constructor.new(_2010.StraightBevelPlanetGear)(method_result) if method_result else None

    def get_part_named_of_type_straight_bevel_sun_gear(self, name: 'str') -> '_2011.StraightBevelSunGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelSunGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2011.StraightBevelSunGear.TYPE](name if name else None)
        return constructor.new(_2011.StraightBevelSunGear)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self, name: 'str') -> '_2012.KlingelnbergCycloPalloidHypoidGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2012.KlingelnbergCycloPalloidHypoidGear.TYPE](name if name else None)
        return constructor.new(_2012.KlingelnbergCycloPalloidHypoidGear)(method_result) if method_result else None

    def get_part_named_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, name: 'str') -> '_2013.KlingelnbergCycloPalloidSpiralBevelGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2013.KlingelnbergCycloPalloidSpiralBevelGear.TYPE](name if name else None)
        return constructor.new(_2013.KlingelnbergCycloPalloidSpiralBevelGear)(method_result) if method_result else None

    def get_part_named_of_type_cylindrical_planet_gear(self, name: 'str') -> '_2014.CylindricalPlanetGear':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalPlanetGear
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2014.CylindricalPlanetGear.TYPE](name if name else None)
        return constructor.new(_2014.CylindricalPlanetGear)(method_result) if method_result else None

    def get_part_named_of_type_clutch_half(self, name: 'str') -> '_2015.ClutchHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ClutchHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2015.ClutchHalf.TYPE](name if name else None)
        return constructor.new(_2015.ClutchHalf)(method_result) if method_result else None

    def get_part_named_of_type_concept_coupling_half(self, name: 'str') -> '_2016.ConceptCouplingHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCouplingHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2016.ConceptCouplingHalf.TYPE](name if name else None)
        return constructor.new(_2016.ConceptCouplingHalf)(method_result) if method_result else None

    def get_part_named_of_type_pulley(self, name: 'str') -> '_2017.Pulley':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.Pulley
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2017.Pulley.TYPE](name if name else None)
        return constructor.new(_2017.Pulley)(method_result) if method_result else None

    def get_part_named_of_type_rolling_ring(self, name: 'str') -> '_2018.RollingRing':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRing
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2018.RollingRing.TYPE](name if name else None)
        return constructor.new(_2018.RollingRing)(method_result) if method_result else None

    def get_part_named_of_type_spring_damper_half(self, name: 'str') -> '_2019.SpringDamperHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamperHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2019.SpringDamperHalf.TYPE](name if name else None)
        return constructor.new(_2019.SpringDamperHalf)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_part(self, name: 'str') -> '_2020.SynchroniserPart':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserPart
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2020.SynchroniserPart.TYPE](name if name else None)
        return constructor.new(_2020.SynchroniserPart)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter_pump(self, name: 'str') -> '_2021.TorqueConverterPump':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverterPump
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2021.TorqueConverterPump.TYPE](name if name else None)
        return constructor.new(_2021.TorqueConverterPump)(method_result) if method_result else None

    def get_part_named_of_type_torque_converter_turbine(self, name: 'str') -> '_2022.TorqueConverterTurbine':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverterTurbine
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2022.TorqueConverterTurbine.TYPE](name if name else None)
        return constructor.new(_2022.TorqueConverterTurbine)(method_result) if method_result else None

    def get_part_named_of_type_cvt_pulley(self, name: 'str') -> '_2023.CVTPulley':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.CVTPulley
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2023.CVTPulley.TYPE](name if name else None)
        return constructor.new(_2023.CVTPulley)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_half(self, name: 'str') -> '_2024.SynchroniserHalf':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserHalf
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2024.SynchroniserHalf.TYPE](name if name else None)
        return constructor.new(_2024.SynchroniserHalf)(method_result) if method_result else None

    def get_part_named_of_type_synchroniser_sleeve(self, name: 'str') -> '_2025.SynchroniserSleeve':
        ''' 'GetPartNamed' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.SynchroniserSleeve
        '''

        name = str(name)
        method_result = self.wrapped.GetPartNamed[_2025.SynchroniserSleeve.TYPE](name if name else None)
        return constructor.new(_2025.SynchroniserSleeve)(method_result) if method_result else None

    def add_part(self, part_type: 'Assembly.PartType', name: 'str') -> '_1931.Part':
        ''' 'AddPart' is the original name of this method.

        Args:
            part_type (mastapy.system_model.part_model.Assembly.PartType)
            name (str)

        Returns:
            mastapy.system_model.part_model.Part
        '''

        part_type = conversion.mp_to_pn_enum(part_type)
        name = str(name)
        method_result = self.wrapped.AddPart(part_type, name if name else None)
        return constructor.new(_1931.Part)(method_result) if method_result else None

    def add_assembly(self, name: Optional['str'] = 'Assembly') -> 'Assembly':
        ''' 'AddAssembly' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.Assembly
        '''

        name = str(name)
        method_result = self.wrapped.AddAssembly(name if name else None)
        return constructor.new(Assembly)(method_result) if method_result else None

    def add_oil_seal(self, name: Optional['str'] = 'Oil Seal') -> '_1929.OilSeal':
        ''' 'AddOilSeal' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.OilSeal
        '''

        name = str(name)
        method_result = self.wrapped.AddOilSeal(name if name else None)
        return constructor.new(_1929.OilSeal)(method_result) if method_result else None

    def add_power_load(self, name: Optional['str'] = 'Power Load') -> '_1934.PowerLoad':
        ''' 'AddPowerLoad' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.PowerLoad
        '''

        name = str(name)
        method_result = self.wrapped.AddPowerLoad(name if name else None)
        return constructor.new(_1934.PowerLoad)(method_result) if method_result else None

    def add_point_load(self, name: Optional['str'] = 'Point Load') -> '_1933.PointLoad':
        ''' 'AddPointLoad' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.PointLoad
        '''

        name = str(name)
        method_result = self.wrapped.AddPointLoad(name if name else None)
        return constructor.new(_1933.PointLoad)(method_result) if method_result else None

    def add_datum(self, name: Optional['str'] = 'Datum') -> '_1916.Datum':
        ''' 'AddDatum' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.Datum
        '''

        name = str(name)
        method_result = self.wrapped.AddDatum(name if name else None)
        return constructor.new(_1916.Datum)(method_result) if method_result else None

    def add_imported_fe_component(self, name: Optional['str'] = 'Imported FE') -> '_1924.ImportedFEComponent':
        ''' 'AddImportedFEComponent' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.ImportedFEComponent
        '''

        name = str(name)
        method_result = self.wrapped.AddImportedFEComponent(name if name else None)
        return constructor.new(_1924.ImportedFEComponent)(method_result) if method_result else None

    def add_measurement_component(self, name: Optional['str'] = 'Measurement Component') -> '_1927.MeasurementComponent':
        ''' 'AddMeasurementComponent' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.MeasurementComponent
        '''

        name = str(name)
        method_result = self.wrapped.AddMeasurementComponent(name if name else None)
        return constructor.new(_1927.MeasurementComponent)(method_result) if method_result else None

    def add_mass_disc(self, name: Optional['str'] = 'Mass Disc') -> '_1926.MassDisc':
        ''' 'AddMassDisc' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.MassDisc
        '''

        name = str(name)
        method_result = self.wrapped.AddMassDisc(name if name else None)
        return constructor.new(_1926.MassDisc)(method_result) if method_result else None

    def add_unbalanced_mass(self, name: Optional['str'] = 'Unbalanced Mass') -> '_1938.UnbalancedMass':
        ''' 'AddUnbalancedMass' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.UnbalancedMass
        '''

        name = str(name)
        method_result = self.wrapped.AddUnbalancedMass(name if name else None)
        return constructor.new(_1938.UnbalancedMass)(method_result) if method_result else None

    def add_straight_bevel_differential_gear_set(self, name: Optional['str'] = 'Straight Bevel Differential Gear Set') -> '_1982.StraightBevelDiffGearSet':
        ''' 'AddStraightBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelDiffGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddStraightBevelDifferentialGearSet(name if name else None)
        return constructor.new(_1982.StraightBevelDiffGearSet)(method_result) if method_result else None

    def add_spiral_bevel_differential_gear_set(self, name: Optional['str'] = 'Spiral Bevel Differential Gear Set') -> '_1981.BevelDifferentialGearSet':
        ''' 'AddSpiralBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddSpiralBevelDifferentialGearSet(name if name else None)
        return constructor.new(_1981.BevelDifferentialGearSet)(method_result) if method_result else None

    def add_zerol_bevel_differential_gear_set(self, name: Optional['str'] = 'Zerol Bevel Differential Gear Set') -> '_1981.BevelDifferentialGearSet':
        ''' 'AddZerolBevelDifferentialGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.BevelDifferentialGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddZerolBevelDifferentialGearSet(name if name else None)
        return constructor.new(_1981.BevelDifferentialGearSet)(method_result) if method_result else None

    def add_planetary_gear_set(self, name: Optional['str'] = 'Planetary Gear Set') -> '_1986.PlanetaryGearSet':
        ''' 'AddPlanetaryGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.PlanetaryGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddPlanetaryGearSet(name if name else None)
        return constructor.new(_1986.PlanetaryGearSet)(method_result) if method_result else None

    def add_spiral_bevel_gear_set(self, name: Optional['str'] = 'Spiral Bevel Gear Set') -> '_1966.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddSpiralBevelGearSet(name if name else None)
        return constructor.new(_1966.SpiralBevelGearSet)(method_result) if method_result else None

    def add_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, name: Optional['str'] = 'Klingelnberg Cyclo Palloid Spiral Bevel Gear Set') -> '_1985.KlingelnbergCycloPalloidSpiralBevelGearSet':
        ''' 'AddKlingelnbergCycloPalloidSpiralBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddKlingelnbergCycloPalloidSpiralBevelGearSet(name if name else None)
        return constructor.new(_1985.KlingelnbergCycloPalloidSpiralBevelGearSet)(method_result) if method_result else None

    def add_klingelnberg_cyclo_palloid_hypoid_gear_set(self, name: Optional['str'] = 'Klingelnberg Cyclo Palloid Hypoid Gear Set') -> '_1984.KlingelnbergCycloPalloidHypoidGearSet':
        ''' 'AddKlingelnbergCycloPalloidHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddKlingelnbergCycloPalloidHypoidGearSet(name if name else None)
        return constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet)(method_result) if method_result else None

    def add_straight_bevel_gear_set(self, name: Optional['str'] = 'Straight Bevel Gear Set') -> '_1964.StraightBevelGearSet':
        ''' 'AddStraightBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.StraightBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddStraightBevelGearSet(name if name else None)
        return constructor.new(_1964.StraightBevelGearSet)(method_result) if method_result else None

    def add_hypoid_gear_set(self, name: Optional['str'] = 'Hypoid Gear Set') -> '_1965.HypoidGearSet':
        ''' 'AddHypoidGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.HypoidGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddHypoidGearSet(name if name else None)
        return constructor.new(_1965.HypoidGearSet)(method_result) if method_result else None

    def add_worm_gear_set(self, name: Optional['str'] = 'Worm Gear Set') -> '_1970.WormGearSet':
        ''' 'AddWormGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.WormGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddWormGearSet(name if name else None)
        return constructor.new(_1970.WormGearSet)(method_result) if method_result else None

    def add_zerol_bevel_gear_set(self, name: Optional['str'] = 'Zerol Bevel Gear Set') -> '_1983.ZerolBevelGearSet':
        ''' 'AddZerolBevelGearSet' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.gears.ZerolBevelGearSet
        '''

        name = str(name)
        method_result = self.wrapped.AddZerolBevelGearSet(name if name else None)
        return constructor.new(_1983.ZerolBevelGearSet)(method_result) if method_result else None

    def add_clutch(self, name: Optional['str'] = 'Clutch') -> '_1988.Clutch':
        ''' 'AddClutch' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.Clutch
        '''

        name = str(name)
        method_result = self.wrapped.AddClutch(name if name else None)
        return constructor.new(_1988.Clutch)(method_result) if method_result else None

    def add_synchroniser(self, name: Optional['str'] = 'Synchroniser') -> '_1976.Synchroniser':
        ''' 'AddSynchroniser' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.Synchroniser
        '''

        name = str(name)
        method_result = self.wrapped.AddSynchroniser(name if name else None)
        return constructor.new(_1976.Synchroniser)(method_result) if method_result else None

    def add_rolling_ring(self, name: Optional['str'] = 'Rolling Ring') -> '_2018.RollingRing':
        ''' 'AddRollingRing' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.RollingRing
        '''

        name = str(name)
        method_result = self.wrapped.AddRollingRing(name if name else None)
        return constructor.new(_2018.RollingRing)(method_result) if method_result else None

    def add_concept_coupling(self, name: Optional['str'] = 'Concept Coupling') -> '_1989.ConceptCoupling':
        ''' 'AddConceptCoupling' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.ConceptCoupling
        '''

        name = str(name)
        method_result = self.wrapped.AddConceptCoupling(name if name else None)
        return constructor.new(_1989.ConceptCoupling)(method_result) if method_result else None

    def add_cvt(self, name: Optional['str'] = 'CVT') -> '_1987.CVT':
        ''' 'AddCVT' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.CVT
        '''

        name = str(name)
        method_result = self.wrapped.AddCVT(name if name else None)
        return constructor.new(_1987.CVT)(method_result) if method_result else None

    def add_spring_damper(self, name: Optional['str'] = 'Spring Damper') -> '_1990.SpringDamper':
        ''' 'AddSpringDamper' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.SpringDamper
        '''

        name = str(name)
        method_result = self.wrapped.AddSpringDamper(name if name else None)
        return constructor.new(_1990.SpringDamper)(method_result) if method_result else None

    def add_torque_converter(self, name: Optional['str'] = 'Torque Converter') -> '_1991.TorqueConverter':
        ''' 'AddTorqueConverter' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.TorqueConverter
        '''

        name = str(name)
        method_result = self.wrapped.AddTorqueConverter(name if name else None)
        return constructor.new(_1991.TorqueConverter)(method_result) if method_result else None

    def add_bolted_joint(self, name: Optional['str'] = 'Bolted Joint') -> '_1911.BoltedJoint':
        ''' 'AddBoltedJoint' is the original name of this method.

        Args:
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.BoltedJoint
        '''

        name = str(name)
        method_result = self.wrapped.AddBoltedJoint(name if name else None)
        return constructor.new(_1911.BoltedJoint)(method_result) if method_result else None

    def add_belt_drive_with_options(self, belt_creation_options: Optional['_2026.BeltCreationOptions'] = None) -> '_1973.BeltDrive':
        ''' 'AddBeltDrive' is the original name of this method.

        Args:
            belt_creation_options (mastapy.system_model.part_model.creation_options.BeltCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        method_result = self.wrapped.AddBeltDrive(belt_creation_options.wrapped if belt_creation_options else None)
        return constructor.new(_1973.BeltDrive)(method_result) if method_result else None

    def add_belt_drive(self, centre_distance: Optional['float'] = 0.1, pulley_a_diameter: Optional['float'] = 0.1, pulley_b_diameter: Optional['float'] = 0.1, name: Optional['str'] = 'Belt Drive') -> '_1973.BeltDrive':
        ''' 'AddBeltDrive' is the original name of this method.

        Args:
            centre_distance (float, optional)
            pulley_a_diameter (float, optional)
            pulley_b_diameter (float, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.couplings.BeltDrive
        '''

        centre_distance = float(centre_distance)
        pulley_a_diameter = float(pulley_a_diameter)
        pulley_b_diameter = float(pulley_b_diameter)
        name = str(name)
        method_result = self.wrapped.AddBeltDrive(centre_distance if centre_distance else 0.0, pulley_a_diameter if pulley_a_diameter else 0.0, pulley_b_diameter if pulley_b_diameter else 0.0, name if name else None)
        return constructor.new(_1973.BeltDrive)(method_result) if method_result else None

    def add_planet_carrier_with_options(self, planet_carrier_creation_options: Optional['_2027.PlanetCarrierCreationOptions'] = None) -> '_1932.PlanetCarrier':
        ''' 'AddPlanetCarrier' is the original name of this method.

        Args:
            planet_carrier_creation_options (mastapy.system_model.part_model.creation_options.PlanetCarrierCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        method_result = self.wrapped.AddPlanetCarrier(planet_carrier_creation_options.wrapped if planet_carrier_creation_options else None)
        return constructor.new(_1932.PlanetCarrier)(method_result) if method_result else None

    def add_planet_carrier(self, number_of_planets: Optional['int'] = 3, diameter: Optional['float'] = 0.1) -> '_1932.PlanetCarrier':
        ''' 'AddPlanetCarrier' is the original name of this method.

        Args:
            number_of_planets (int, optional)
            diameter (float, optional)

        Returns:
            mastapy.system_model.part_model.PlanetCarrier
        '''

        number_of_planets = int(number_of_planets)
        diameter = float(diameter)
        method_result = self.wrapped.AddPlanetCarrier(number_of_planets if number_of_planets else 0, diameter if diameter else 0.0)
        return constructor.new(_1932.PlanetCarrier)(method_result) if method_result else None

    def add_shaft_with_options(self, shaft_creation_options: '_2028.ShaftCreationOptions') -> '_1942.Shaft':
        ''' 'AddShaft' is the original name of this method.

        Args:
            shaft_creation_options (mastapy.system_model.part_model.creation_options.ShaftCreationOptions)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        method_result = self.wrapped.AddShaft(shaft_creation_options.wrapped if shaft_creation_options else None)
        return constructor.new(_1942.Shaft)(method_result) if method_result else None

    def add_shaft(self, length: Optional['float'] = 0.1, outer_diameter: Optional['float'] = 0.0, bore: Optional['float'] = 0.0, name: Optional['str'] = 'Shaft') -> '_1942.Shaft':
        ''' 'AddShaft' is the original name of this method.

        Args:
            length (float, optional)
            outer_diameter (float, optional)
            bore (float, optional)
            name (str, optional)

        Returns:
            mastapy.system_model.part_model.shaft_model.Shaft
        '''

        length = float(length)
        outer_diameter = float(outer_diameter)
        bore = float(bore)
        name = str(name)
        method_result = self.wrapped.AddShaft(length if length else 0.0, outer_diameter if outer_diameter else 0.0, bore if bore else 0.0, name if name else None)
        return constructor.new(_1942.Shaft)(method_result) if method_result else None

    def add_cylindrical_gear_pair_with_options(self, cylindrical_gear_pair_creation_options: Optional['_1066.CylindricalGearPairCreationOptions'] = None) -> '_1968.CylindricalGearSet':
        ''' 'AddCylindricalGearPair' is the original name of this method.

        Args:
            cylindrical_gear_pair_creation_options (mastapy.gears.gear_designs.creation_options.CylindricalGearPairCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        method_result = self.wrapped.AddCylindricalGearPair(cylindrical_gear_pair_creation_options.wrapped if cylindrical_gear_pair_creation_options else None)
        return constructor.new(_1968.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_pair(self, centre_distance: 'float') -> '_1968.CylindricalGearSet':
        ''' 'AddCylindricalGearPair' is the original name of this method.

        Args:
            centre_distance (float)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        centre_distance = float(centre_distance)
        method_result = self.wrapped.AddCylindricalGearPair(centre_distance if centre_distance else 0.0)
        return constructor.new(_1968.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_set_with_options(self, cylindrical_gear_linear_train_creation_options: Optional['_2029.CylindricalGearLinearTrainCreationOptions'] = None) -> '_1968.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            cylindrical_gear_linear_train_creation_options (mastapy.system_model.part_model.creation_options.CylindricalGearLinearTrainCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        method_result = self.wrapped.AddCylindricalGearSet(cylindrical_gear_linear_train_creation_options.wrapped if cylindrical_gear_linear_train_creation_options else None)
        return constructor.new(_1968.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_set(self, name: 'str', centre_distances: 'List[float]') -> '_1968.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            name (str)
            centre_distances (List[float])

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        centre_distances = conversion.mp_to_pn_list_float(centre_distances)
        method_result = self.wrapped.AddCylindricalGearSet(name if name else None, centre_distances)
        return constructor.new(_1968.CylindricalGearSet)(method_result) if method_result else None

    def add_cylindrical_gear_set_extended(self, name: 'str', normal_pressure_angle: 'float', helix_angle: 'float', normal_module: 'float', pinion_hand: '_305.Hand', centre_distances: 'List[float]') -> '_1968.CylindricalGearSet':
        ''' 'AddCylindricalGearSet' is the original name of this method.

        Args:
            name (str)
            normal_pressure_angle (float)
            helix_angle (float)
            normal_module (float)
            pinion_hand (mastapy.gears.Hand)
            centre_distances (List[float])

        Returns:
            mastapy.system_model.part_model.gears.CylindricalGearSet
        '''

        name = str(name)
        normal_pressure_angle = float(normal_pressure_angle)
        helix_angle = float(helix_angle)
        normal_module = float(normal_module)
        pinion_hand = conversion.mp_to_pn_enum(pinion_hand)
        centre_distances = conversion.mp_to_pn_list_float(centre_distances)
        method_result = self.wrapped.AddCylindricalGearSet(name if name else None, normal_pressure_angle if normal_pressure_angle else 0.0, helix_angle if helix_angle else 0.0, normal_module if normal_module else 0.0, pinion_hand, centre_distances)
        return constructor.new(_1968.CylindricalGearSet)(method_result) if method_result else None

    def add_spiral_bevel_gear_set_with_options(self, spiral_bevel_gear_set_creation_options: Optional['_1069.SpiralBevelGearSetCreationOptions'] = None) -> '_1966.SpiralBevelGearSet':
        ''' 'AddSpiralBevelGearSet' is the original name of this method.

        Args:
            spiral_bevel_gear_set_creation_options (mastapy.gears.gear_designs.creation_options.SpiralBevelGearSetCreationOptions, optional)

        Returns:
            mastapy.system_model.part_model.gears.SpiralBevelGearSet
        '''

        method_result = self.wrapped.AddSpiralBevelGearSet(spiral_bevel_gear_set_creation_options.wrapped if spiral_bevel_gear_set_creation_options else None)
        return constructor.new(_1966.SpiralBevelGearSet)(method_result) if method_result else None

    def add_bearing(self, name: 'str') -> '_1908.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        method_result = self.wrapped.AddBearing(name if name else None)
        return constructor.new(_1908.Bearing)(method_result) if method_result else None

    def import_fe_mesh_from_file(self, file_name: 'str', stiffness_matrix: '_109.NodalMatrix') -> '_1924.ImportedFEComponent':
        ''' 'ImportFEMeshFromFile' is the original name of this method.

        Args:
            file_name (str)
            stiffness_matrix (mastapy.nodal_analysis.NodalMatrix)

        Returns:
            mastapy.system_model.part_model.ImportedFEComponent
        '''

        file_name = str(file_name)
        method_result = self.wrapped.ImportFEMeshFromFile(file_name if file_name else None, stiffness_matrix.wrapped if stiffness_matrix else None)
        return constructor.new(_1924.ImportedFEComponent)(method_result) if method_result else None

    def all_parts_of_type_abstract_assembly(self) -> 'List[_1905.AbstractAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1905.AbstractAssembly.TYPE](), constructor.new(_1905.AbstractAssembly))

    def all_parts_of_type_component(self) -> 'List[_1912.Component]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Component]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1912.Component.TYPE](), constructor.new(_1912.Component))

    def all_parts_of_type_assembly(self) -> 'List[Assembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Assembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[Assembly.TYPE](), constructor.new(Assembly))

    def all_parts_of_type_specialised_assembly(self) -> 'List[_1937.SpecialisedAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.SpecialisedAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1937.SpecialisedAssembly.TYPE](), constructor.new(_1937.SpecialisedAssembly))

    def all_parts_of_type_root_assembly(self) -> 'List[_1935.RootAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.RootAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1935.RootAssembly.TYPE](), constructor.new(_1935.RootAssembly))

    def all_parts_of_type_bolted_joint(self) -> 'List[_1911.BoltedJoint]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.BoltedJoint]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1911.BoltedJoint.TYPE](), constructor.new(_1911.BoltedJoint))

    def all_parts_of_type_flexible_pin_assembly(self) -> 'List[_1920.FlexiblePinAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.FlexiblePinAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1920.FlexiblePinAssembly.TYPE](), constructor.new(_1920.FlexiblePinAssembly))

    def all_parts_of_type_gear_set(self) -> 'List[_1972.GearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.GearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1972.GearSet.TYPE](), constructor.new(_1972.GearSet))

    def all_parts_of_type_belt_drive(self) -> 'List[_1973.BeltDrive]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.BeltDrive]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1973.BeltDrive.TYPE](), constructor.new(_1973.BeltDrive))

    def all_parts_of_type_coupling(self) -> 'List[_1974.Coupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Coupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1974.Coupling.TYPE](), constructor.new(_1974.Coupling))

    def all_parts_of_type_rolling_ring_assembly(self) -> 'List[_1975.RollingRingAssembly]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.RollingRingAssembly]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1975.RollingRingAssembly.TYPE](), constructor.new(_1975.RollingRingAssembly))

    def all_parts_of_type_synchroniser(self) -> 'List[_1976.Synchroniser]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Synchroniser]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1976.Synchroniser.TYPE](), constructor.new(_1976.Synchroniser))

    def all_parts_of_type_concept_gear_set(self) -> 'List[_1977.ConceptGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConceptGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1977.ConceptGearSet.TYPE](), constructor.new(_1977.ConceptGearSet))

    def all_parts_of_type_conical_gear_set(self) -> 'List[_1969.ConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1969.ConicalGearSet.TYPE](), constructor.new(_1969.ConicalGearSet))

    def all_parts_of_type_cylindrical_gear_set(self) -> 'List[_1968.CylindricalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1968.CylindricalGearSet.TYPE](), constructor.new(_1968.CylindricalGearSet))

    def all_parts_of_type_face_gear_set(self) -> 'List[_1978.FaceGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.FaceGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1978.FaceGearSet.TYPE](), constructor.new(_1978.FaceGearSet))

    def all_parts_of_type_worm_gear_set(self) -> 'List[_1970.WormGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.WormGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1970.WormGearSet.TYPE](), constructor.new(_1970.WormGearSet))

    def all_parts_of_type_agma_gleason_conical_gear_set(self) -> 'List[_1979.AGMAGleasonConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1979.AGMAGleasonConicalGearSet.TYPE](), constructor.new(_1979.AGMAGleasonConicalGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear_set(self) -> 'List[_1971.KlingelnbergCycloPalloidConicalGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1971.KlingelnbergCycloPalloidConicalGearSet.TYPE](), constructor.new(_1971.KlingelnbergCycloPalloidConicalGearSet))

    def all_parts_of_type_bevel_gear_set(self) -> 'List[_1980.BevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1980.BevelGearSet.TYPE](), constructor.new(_1980.BevelGearSet))

    def all_parts_of_type_hypoid_gear_set(self) -> 'List[_1965.HypoidGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.HypoidGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1965.HypoidGearSet.TYPE](), constructor.new(_1965.HypoidGearSet))

    def all_parts_of_type_bevel_differential_gear_set(self) -> 'List[_1981.BevelDifferentialGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1981.BevelDifferentialGearSet.TYPE](), constructor.new(_1981.BevelDifferentialGearSet))

    def all_parts_of_type_spiral_bevel_gear_set(self) -> 'List[_1966.SpiralBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.SpiralBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1966.SpiralBevelGearSet.TYPE](), constructor.new(_1966.SpiralBevelGearSet))

    def all_parts_of_type_straight_bevel_diff_gear_set(self) -> 'List[_1982.StraightBevelDiffGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelDiffGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1982.StraightBevelDiffGearSet.TYPE](), constructor.new(_1982.StraightBevelDiffGearSet))

    def all_parts_of_type_straight_bevel_gear_set(self) -> 'List[_1964.StraightBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1964.StraightBevelGearSet.TYPE](), constructor.new(_1964.StraightBevelGearSet))

    def all_parts_of_type_zerol_bevel_gear_set(self) -> 'List[_1983.ZerolBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ZerolBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1983.ZerolBevelGearSet.TYPE](), constructor.new(_1983.ZerolBevelGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set(self) -> 'List[_1984.KlingelnbergCycloPalloidHypoidGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1984.KlingelnbergCycloPalloidHypoidGearSet.TYPE](), constructor.new(_1984.KlingelnbergCycloPalloidHypoidGearSet))

    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self) -> 'List[_1985.KlingelnbergCycloPalloidSpiralBevelGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1985.KlingelnbergCycloPalloidSpiralBevelGearSet.TYPE](), constructor.new(_1985.KlingelnbergCycloPalloidSpiralBevelGearSet))

    def all_parts_of_type_planetary_gear_set(self) -> 'List[_1986.PlanetaryGearSet]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.PlanetaryGearSet]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1986.PlanetaryGearSet.TYPE](), constructor.new(_1986.PlanetaryGearSet))

    def all_parts_of_type_cvt(self) -> 'List[_1987.CVT]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CVT]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1987.CVT.TYPE](), constructor.new(_1987.CVT))

    def all_parts_of_type_clutch(self) -> 'List[_1988.Clutch]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Clutch]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1988.Clutch.TYPE](), constructor.new(_1988.Clutch))

    def all_parts_of_type_concept_coupling(self) -> 'List[_1989.ConceptCoupling]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ConceptCoupling]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1989.ConceptCoupling.TYPE](), constructor.new(_1989.ConceptCoupling))

    def all_parts_of_type_spring_damper(self) -> 'List[_1990.SpringDamper]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SpringDamper]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1990.SpringDamper.TYPE](), constructor.new(_1990.SpringDamper))

    def all_parts_of_type_torque_converter(self) -> 'List[_1991.TorqueConverter]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverter]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1991.TorqueConverter.TYPE](), constructor.new(_1991.TorqueConverter))

    def all_parts_of_type_abstract_shaft_or_housing(self) -> 'List[_1906.AbstractShaftOrHousing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.AbstractShaftOrHousing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1906.AbstractShaftOrHousing.TYPE](), constructor.new(_1906.AbstractShaftOrHousing))

    def all_parts_of_type_bolt(self) -> 'List[_1910.Bolt]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Bolt]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1910.Bolt.TYPE](), constructor.new(_1910.Bolt))

    def all_parts_of_type_datum(self) -> 'List[_1916.Datum]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Datum]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1916.Datum.TYPE](), constructor.new(_1916.Datum))

    def all_parts_of_type_external_cad_model(self) -> 'List[_1919.ExternalCADModel]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.ExternalCADModel]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1919.ExternalCADModel.TYPE](), constructor.new(_1919.ExternalCADModel))

    def all_parts_of_type_guide_dxf_model(self) -> 'List[_1921.GuideDxfModel]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.GuideDxfModel]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1921.GuideDxfModel.TYPE](), constructor.new(_1921.GuideDxfModel))

    def all_parts_of_type_mountable_component(self) -> 'List[_1928.MountableComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MountableComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1928.MountableComponent.TYPE](), constructor.new(_1928.MountableComponent))

    def all_parts_of_type_imported_fe_component(self) -> 'List[_1924.ImportedFEComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.ImportedFEComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1924.ImportedFEComponent.TYPE](), constructor.new(_1924.ImportedFEComponent))

    def all_parts_of_type_shaft(self) -> 'List[_1942.Shaft]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.shaft_model.Shaft]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1942.Shaft.TYPE](), constructor.new(_1942.Shaft))

    def all_parts_of_type_connector(self) -> 'List[_1915.Connector]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Connector]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1915.Connector.TYPE](), constructor.new(_1915.Connector))

    def all_parts_of_type_planet_carrier(self) -> 'List[_1932.PlanetCarrier]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PlanetCarrier]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1932.PlanetCarrier.TYPE](), constructor.new(_1932.PlanetCarrier))

    def all_parts_of_type_virtual_component(self) -> 'List[_1939.VirtualComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.VirtualComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1939.VirtualComponent.TYPE](), constructor.new(_1939.VirtualComponent))

    def all_parts_of_type_gear(self) -> 'List[_1992.Gear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.Gear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1992.Gear.TYPE](), constructor.new(_1992.Gear))

    def all_parts_of_type_coupling_half(self) -> 'List[_1993.CouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1993.CouplingHalf.TYPE](), constructor.new(_1993.CouplingHalf))

    def all_parts_of_type_bearing(self) -> 'List[_1908.Bearing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.Bearing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1908.Bearing.TYPE](), constructor.new(_1908.Bearing))

    def all_parts_of_type_oil_seal(self) -> 'List[_1929.OilSeal]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.OilSeal]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1929.OilSeal.TYPE](), constructor.new(_1929.OilSeal))

    def all_parts_of_type_shaft_hub_connection(self) -> 'List[_1967.ShaftHubConnection]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ShaftHubConnection]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1967.ShaftHubConnection.TYPE](), constructor.new(_1967.ShaftHubConnection))

    def all_parts_of_type_mass_disc(self) -> 'List[_1926.MassDisc]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MassDisc]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1926.MassDisc.TYPE](), constructor.new(_1926.MassDisc))

    def all_parts_of_type_measurement_component(self) -> 'List[_1927.MeasurementComponent]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.MeasurementComponent]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1927.MeasurementComponent.TYPE](), constructor.new(_1927.MeasurementComponent))

    def all_parts_of_type_point_load(self) -> 'List[_1933.PointLoad]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PointLoad]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1933.PointLoad.TYPE](), constructor.new(_1933.PointLoad))

    def all_parts_of_type_power_load(self) -> 'List[_1934.PowerLoad]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.PowerLoad]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1934.PowerLoad.TYPE](), constructor.new(_1934.PowerLoad))

    def all_parts_of_type_unbalanced_mass(self) -> 'List[_1938.UnbalancedMass]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.UnbalancedMass]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1938.UnbalancedMass.TYPE](), constructor.new(_1938.UnbalancedMass))

    def all_parts_of_type_concept_gear(self) -> 'List[_1994.ConceptGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConceptGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1994.ConceptGear.TYPE](), constructor.new(_1994.ConceptGear))

    def all_parts_of_type_conical_gear(self) -> 'List[_1995.ConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1995.ConicalGear.TYPE](), constructor.new(_1995.ConicalGear))

    def all_parts_of_type_cylindrical_gear(self) -> 'List[_1996.CylindricalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1996.CylindricalGear.TYPE](), constructor.new(_1996.CylindricalGear))

    def all_parts_of_type_face_gear(self) -> 'List[_1997.FaceGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.FaceGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1997.FaceGear.TYPE](), constructor.new(_1997.FaceGear))

    def all_parts_of_type_worm_gear(self) -> 'List[_1998.WormGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.WormGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1998.WormGear.TYPE](), constructor.new(_1998.WormGear))

    def all_parts_of_type_agma_gleason_conical_gear(self) -> 'List[_1999.AGMAGleasonConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.AGMAGleasonConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_1999.AGMAGleasonConicalGear.TYPE](), constructor.new(_1999.AGMAGleasonConicalGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> 'List[_2000.KlingelnbergCycloPalloidConicalGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2000.KlingelnbergCycloPalloidConicalGear.TYPE](), constructor.new(_2000.KlingelnbergCycloPalloidConicalGear))

    def all_parts_of_type_bevel_gear(self) -> 'List[_2001.BevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2001.BevelGear.TYPE](), constructor.new(_2001.BevelGear))

    def all_parts_of_type_hypoid_gear(self) -> 'List[_2002.HypoidGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.HypoidGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2002.HypoidGear.TYPE](), constructor.new(_2002.HypoidGear))

    def all_parts_of_type_bevel_differential_gear(self) -> 'List[_2003.BevelDifferentialGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2003.BevelDifferentialGear.TYPE](), constructor.new(_2003.BevelDifferentialGear))

    def all_parts_of_type_spiral_bevel_gear(self) -> 'List[_2004.SpiralBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.SpiralBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2004.SpiralBevelGear.TYPE](), constructor.new(_2004.SpiralBevelGear))

    def all_parts_of_type_straight_bevel_diff_gear(self) -> 'List[_2005.StraightBevelDiffGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelDiffGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2005.StraightBevelDiffGear.TYPE](), constructor.new(_2005.StraightBevelDiffGear))

    def all_parts_of_type_straight_bevel_gear(self) -> 'List[_2006.StraightBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2006.StraightBevelGear.TYPE](), constructor.new(_2006.StraightBevelGear))

    def all_parts_of_type_zerol_bevel_gear(self) -> 'List[_2007.ZerolBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.ZerolBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2007.ZerolBevelGear.TYPE](), constructor.new(_2007.ZerolBevelGear))

    def all_parts_of_type_bevel_differential_planet_gear(self) -> 'List[_2008.BevelDifferentialPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2008.BevelDifferentialPlanetGear.TYPE](), constructor.new(_2008.BevelDifferentialPlanetGear))

    def all_parts_of_type_bevel_differential_sun_gear(self) -> 'List[_2009.BevelDifferentialSunGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.BevelDifferentialSunGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2009.BevelDifferentialSunGear.TYPE](), constructor.new(_2009.BevelDifferentialSunGear))

    def all_parts_of_type_straight_bevel_planet_gear(self) -> 'List[_2010.StraightBevelPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2010.StraightBevelPlanetGear.TYPE](), constructor.new(_2010.StraightBevelPlanetGear))

    def all_parts_of_type_straight_bevel_sun_gear(self) -> 'List[_2011.StraightBevelSunGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.StraightBevelSunGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2011.StraightBevelSunGear.TYPE](), constructor.new(_2011.StraightBevelSunGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> 'List[_2012.KlingelnbergCycloPalloidHypoidGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2012.KlingelnbergCycloPalloidHypoidGear.TYPE](), constructor.new(_2012.KlingelnbergCycloPalloidHypoidGear))

    def all_parts_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> 'List[_2013.KlingelnbergCycloPalloidSpiralBevelGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2013.KlingelnbergCycloPalloidSpiralBevelGear.TYPE](), constructor.new(_2013.KlingelnbergCycloPalloidSpiralBevelGear))

    def all_parts_of_type_cylindrical_planet_gear(self) -> 'List[_2014.CylindricalPlanetGear]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.gears.CylindricalPlanetGear]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2014.CylindricalPlanetGear.TYPE](), constructor.new(_2014.CylindricalPlanetGear))

    def all_parts_of_type_clutch_half(self) -> 'List[_2015.ClutchHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ClutchHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2015.ClutchHalf.TYPE](), constructor.new(_2015.ClutchHalf))

    def all_parts_of_type_concept_coupling_half(self) -> 'List[_2016.ConceptCouplingHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.ConceptCouplingHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2016.ConceptCouplingHalf.TYPE](), constructor.new(_2016.ConceptCouplingHalf))

    def all_parts_of_type_pulley(self) -> 'List[_2017.Pulley]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.Pulley]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2017.Pulley.TYPE](), constructor.new(_2017.Pulley))

    def all_parts_of_type_rolling_ring(self) -> 'List[_2018.RollingRing]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.RollingRing]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2018.RollingRing.TYPE](), constructor.new(_2018.RollingRing))

    def all_parts_of_type_spring_damper_half(self) -> 'List[_2019.SpringDamperHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SpringDamperHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2019.SpringDamperHalf.TYPE](), constructor.new(_2019.SpringDamperHalf))

    def all_parts_of_type_synchroniser_part(self) -> 'List[_2020.SynchroniserPart]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserPart]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2020.SynchroniserPart.TYPE](), constructor.new(_2020.SynchroniserPart))

    def all_parts_of_type_torque_converter_pump(self) -> 'List[_2021.TorqueConverterPump]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverterPump]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2021.TorqueConverterPump.TYPE](), constructor.new(_2021.TorqueConverterPump))

    def all_parts_of_type_torque_converter_turbine(self) -> 'List[_2022.TorqueConverterTurbine]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.TorqueConverterTurbine]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2022.TorqueConverterTurbine.TYPE](), constructor.new(_2022.TorqueConverterTurbine))

    def all_parts_of_type_cvt_pulley(self) -> 'List[_2023.CVTPulley]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.CVTPulley]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2023.CVTPulley.TYPE](), constructor.new(_2023.CVTPulley))

    def all_parts_of_type_synchroniser_half(self) -> 'List[_2024.SynchroniserHalf]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserHalf]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2024.SynchroniserHalf.TYPE](), constructor.new(_2024.SynchroniserHalf))

    def all_parts_of_type_synchroniser_sleeve(self) -> 'List[_2025.SynchroniserSleeve]':
        ''' 'AllParts' is the original name of this method.

        Returns:
            List[mastapy.system_model.part_model.couplings.SynchroniserSleeve]
        '''

        return conversion.pn_to_mp_objects_in_list(self.wrapped.AllParts[_2025.SynchroniserSleeve.TYPE](), constructor.new(_2025.SynchroniserSleeve))

    def add_axial_clearance_bearing(self, name: 'str', contact_diameter: 'float') -> '_1908.Bearing':
        ''' 'AddAxialClearanceBearing' is the original name of this method.

        Args:
            name (str)
            contact_diameter (float)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        contact_diameter = float(contact_diameter)
        method_result = self.wrapped.AddAxialClearanceBearing(name if name else None, contact_diameter if contact_diameter else 0.0)
        return constructor.new(_1908.Bearing)(method_result) if method_result else None

    def add_shaft_hub_connection(self, name: 'str') -> '_1967.ShaftHubConnection':
        ''' 'AddShaftHubConnection' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.system_model.part_model.couplings.ShaftHubConnection
        '''

        name = str(name)
        method_result = self.wrapped.AddShaftHubConnection(name if name else None)
        return constructor.new(_1967.ShaftHubConnection)(method_result) if method_result else None

    def add_rolling_bearing_from_catalogue(self, catalogue: '_1460.BearingCatalog', designation: 'str', name: 'str') -> '_1908.Bearing':
        ''' 'AddRollingBearingFromCatalogue' is the original name of this method.

        Args:
            catalogue (mastapy.bearings.BearingCatalog)
            designation (str)
            name (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        catalogue = conversion.mp_to_pn_enum(catalogue)
        designation = str(designation)
        name = str(name)
        method_result = self.wrapped.AddRollingBearingFromCatalogue(catalogue, designation if designation else None, name if name else None)
        return constructor.new(_1908.Bearing)(method_result) if method_result else None

    def add_bearing_with_name_and_rolling_bearing_type(self, name: 'str', type_: '_1484.RollingBearingType') -> '_1908.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)
            type_ (mastapy.bearings.RollingBearingType)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        type_ = conversion.mp_to_pn_enum(type_)
        method_result = self.wrapped.AddBearing(name if name else None, type_)
        return constructor.new(_1908.Bearing)(method_result) if method_result else None

    def add_bearing_with_name_rolling_bearing_type_and_designation(self, name: 'str', type_: '_1484.RollingBearingType', designation: 'str') -> '_1908.Bearing':
        ''' 'AddBearing' is the original name of this method.

        Args:
            name (str)
            type_ (mastapy.bearings.RollingBearingType)
            designation (str)

        Returns:
            mastapy.system_model.part_model.Bearing
        '''

        name = str(name)
        type_ = conversion.mp_to_pn_enum(type_)
        designation = str(designation)
        method_result = self.wrapped.AddBearing(name if name else None, type_, designation if designation else None)
        return constructor.new(_1908.Bearing)(method_result) if method_result else None
