'''_1699.py

RollingBearing
'''


from typing import Callable

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.bearings import (
    _1481, _1483, _1460, _1471,
    _1486, _1462
)
from mastapy.bearings.bearing_designs.rolling import (
    _1701, _1693, _1692, _1691,
    _1700, _1688
)
from mastapy._internal.python_net import python_net_import
from mastapy.utility import _1264
from mastapy.materials import _233
from mastapy.bearings.bearing_designs import _1683

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_ROLLING_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.Rolling', 'RollingBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingBearing',)


class RollingBearing(_1683.DetailedBearing):
    '''RollingBearing

    This is a mastapy class.
    '''

    TYPE = _ROLLING_BEARING
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingBearing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def no_history(self) -> 'str':
        '''str: 'NoHistory' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NoHistory

    @property
    def arrangement(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement':
        '''enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement: 'Arrangement' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement)(self.wrapped.Arrangement) if self.wrapped.Arrangement else None

    @arrangement.setter
    def arrangement(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.Arrangement = value

    @property
    def width(self) -> 'float':
        '''float: 'Width' is the original name of this property.'''

        return self.wrapped.Width

    @width.setter
    def width(self, value: 'float'):
        self.wrapped.Width = float(value) if value else 0.0

    @property
    def inner_ring_width(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'InnerRingWidth' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.InnerRingWidth) if self.wrapped.InnerRingWidth else None

    @inner_ring_width.setter
    def inner_ring_width(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.InnerRingWidth = value

    @property
    def outer_ring_width(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OuterRingWidth' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OuterRingWidth) if self.wrapped.OuterRingWidth else None

    @outer_ring_width.setter
    def outer_ring_width(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.OuterRingWidth = value

    @property
    def outer_ring_offset(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'OuterRingOffset' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.OuterRingOffset) if self.wrapped.OuterRingOffset else None

    @outer_ring_offset.setter
    def outer_ring_offset(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.OuterRingOffset = value

    @property
    def inner_race_outer_diameter(self) -> 'float':
        '''float: 'InnerRaceOuterDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.InnerRaceOuterDiameter

    @property
    def outer_race_inner_diameter(self) -> 'float':
        '''float: 'OuterRaceInnerDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OuterRaceInnerDiameter

    @property
    def inner_race_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType':
        '''enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType: 'InnerRaceType' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType)(self.wrapped.InnerRaceType) if self.wrapped.InnerRaceType else None

    @inner_race_type.setter
    def inner_race_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.InnerRaceType = value

    @property
    def outer_race_type(self) -> 'enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType':
        '''enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType: 'OuterRaceType' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType)(self.wrapped.OuterRaceType) if self.wrapped.OuterRaceType else None

    @outer_race_type.setter
    def outer_race_type(self, value: 'enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.OuterRaceType = value

    @property
    def catalogue(self) -> '_1460.BearingCatalog':
        '''BearingCatalog: 'Catalogue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.Catalogue)
        return constructor.new(_1460.BearingCatalog)(value) if value else None

    @property
    def designation(self) -> 'str':
        '''str: 'Designation' is the original name of this property.'''

        return self.wrapped.Designation

    @designation.setter
    def designation(self, value: 'str'):
        self.wrapped.Designation = str(value) if value else None

    @property
    def manufacturer(self) -> 'str':
        '''str: 'Manufacturer' is the original name of this property.'''

        return self.wrapped.Manufacturer

    @manufacturer.setter
    def manufacturer(self, value: 'str'):
        self.wrapped.Manufacturer = str(value) if value else None

    @property
    def width_series(self) -> 'overridable.Overridable_WidthSeries':
        '''overridable.Overridable_WidthSeries: 'WidthSeries' is the original name of this property.'''

        return constructor.new(overridable.Overridable_WidthSeries)(self.wrapped.WidthSeries) if self.wrapped.WidthSeries else None

    @width_series.setter
    def width_series(self, value: 'overridable.Overridable_WidthSeries.implicit_type()'):
        wrapper_type = overridable.Overridable_WidthSeries.TYPE
        enclosed_type = overridable.Overridable_WidthSeries.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.WidthSeries = value

    @property
    def height_series(self) -> 'overridable.Overridable_HeightSeries':
        '''overridable.Overridable_HeightSeries: 'HeightSeries' is the original name of this property.'''

        return constructor.new(overridable.Overridable_HeightSeries)(self.wrapped.HeightSeries) if self.wrapped.HeightSeries else None

    @height_series.setter
    def height_series(self, value: 'overridable.Overridable_HeightSeries.implicit_type()'):
        wrapper_type = overridable.Overridable_HeightSeries.TYPE
        enclosed_type = overridable.Overridable_HeightSeries.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.HeightSeries = value

    @property
    def diameter_series(self) -> 'overridable.Overridable_DiameterSeries':
        '''overridable.Overridable_DiameterSeries: 'DiameterSeries' is the original name of this property.'''

        return constructor.new(overridable.Overridable_DiameterSeries)(self.wrapped.DiameterSeries) if self.wrapped.DiameterSeries else None

    @diameter_series.setter
    def diameter_series(self, value: 'overridable.Overridable_DiameterSeries.implicit_type()'):
        wrapper_type = overridable.Overridable_DiameterSeries.TYPE
        enclosed_type = overridable.Overridable_DiameterSeries.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.DiameterSeries = value

    @property
    def fatigue_load_limit(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'FatigueLoadLimit' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.FatigueLoadLimit) if self.wrapped.FatigueLoadLimit else None

    @fatigue_load_limit.setter
    def fatigue_load_limit(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.FatigueLoadLimit = value

    @property
    def is_full_complement(self) -> 'bool':
        '''bool: 'IsFullComplement' is the original name of this property.'''

        return self.wrapped.IsFullComplement

    @is_full_complement.setter
    def is_full_complement(self, value: 'bool'):
        self.wrapped.IsFullComplement = bool(value) if value else False

    @property
    def type_(self) -> 'str':
        '''str: 'Type' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Type

    @property
    def number_of_rows(self) -> 'int':
        '''int: 'NumberOfRows' is the original name of this property.'''

        return self.wrapped.NumberOfRows

    @number_of_rows.setter
    def number_of_rows(self, value: 'int'):
        self.wrapped.NumberOfRows = int(value) if value else 0

    @property
    def maximum_oil_speed(self) -> 'float':
        '''float: 'MaximumOilSpeed' is the original name of this property.'''

        return self.wrapped.MaximumOilSpeed

    @maximum_oil_speed.setter
    def maximum_oil_speed(self, value: 'float'):
        self.wrapped.MaximumOilSpeed = float(value) if value else 0.0

    @property
    def maximum_grease_speed(self) -> 'float':
        '''float: 'MaximumGreaseSpeed' is the original name of this property.'''

        return self.wrapped.MaximumGreaseSpeed

    @maximum_grease_speed.setter
    def maximum_grease_speed(self, value: 'float'):
        self.wrapped.MaximumGreaseSpeed = float(value) if value else 0.0

    @property
    def element_material_reportable(self) -> 'str':
        '''str: 'ElementMaterialReportable' is the original name of this property.'''

        return self.wrapped.ElementMaterialReportable.SelectedItemName

    @element_material_reportable.setter
    def element_material_reportable(self, value: 'str'):
        self.wrapped.ElementMaterialReportable.SetSelectedItem(str(value) if value else None)

    @property
    def inner_race_material_reportable(self) -> 'str':
        '''str: 'InnerRaceMaterialReportable' is the original name of this property.'''

        return self.wrapped.InnerRaceMaterialReportable.SelectedItemName

    @inner_race_material_reportable.setter
    def inner_race_material_reportable(self, value: 'str'):
        self.wrapped.InnerRaceMaterialReportable.SetSelectedItem(str(value) if value else None)

    @property
    def outer_race_material_reportable(self) -> 'str':
        '''str: 'OuterRaceMaterialReportable' is the original name of this property.'''

        return self.wrapped.OuterRaceMaterialReportable.SelectedItemName

    @outer_race_material_reportable.setter
    def outer_race_material_reportable(self, value: 'str'):
        self.wrapped.OuterRaceMaterialReportable.SetSelectedItem(str(value) if value else None)

    @property
    def inner_race_hardness_depth(self) -> 'float':
        '''float: 'InnerRaceHardnessDepth' is the original name of this property.'''

        return self.wrapped.InnerRaceHardnessDepth

    @inner_race_hardness_depth.setter
    def inner_race_hardness_depth(self, value: 'float'):
        self.wrapped.InnerRaceHardnessDepth = float(value) if value else 0.0

    @property
    def outer_race_hardness_depth(self) -> 'float':
        '''float: 'OuterRaceHardnessDepth' is the original name of this property.'''

        return self.wrapped.OuterRaceHardnessDepth

    @outer_race_hardness_depth.setter
    def outer_race_hardness_depth(self, value: 'float'):
        self.wrapped.OuterRaceHardnessDepth = float(value) if value else 0.0

    @property
    def element_surface_roughness_ra(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementSurfaceRoughnessRa' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementSurfaceRoughnessRa) if self.wrapped.ElementSurfaceRoughnessRa else None

    @element_surface_roughness_ra.setter
    def element_surface_roughness_ra(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ElementSurfaceRoughnessRa = value

    @property
    def element_surface_roughness_rms(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementSurfaceRoughnessRMS' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementSurfaceRoughnessRMS) if self.wrapped.ElementSurfaceRoughnessRMS else None

    @element_surface_roughness_rms.setter
    def element_surface_roughness_rms(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ElementSurfaceRoughnessRMS = value

    @property
    def minimum_surface_roughness_ra(self) -> 'float':
        '''float: 'MinimumSurfaceRoughnessRa' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumSurfaceRoughnessRa

    @property
    def minimum_surface_roughness_rms(self) -> 'float':
        '''float: 'MinimumSurfaceRoughnessRMS' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MinimumSurfaceRoughnessRMS

    @property
    def raceway_surface_roughness_ra_inner(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RacewaySurfaceRoughnessRaInner' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RacewaySurfaceRoughnessRaInner) if self.wrapped.RacewaySurfaceRoughnessRaInner else None

    @raceway_surface_roughness_ra_inner.setter
    def raceway_surface_roughness_ra_inner(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RacewaySurfaceRoughnessRaInner = value

    @property
    def raceway_surface_roughness_ra_outer(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RacewaySurfaceRoughnessRaOuter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RacewaySurfaceRoughnessRaOuter) if self.wrapped.RacewaySurfaceRoughnessRaOuter else None

    @raceway_surface_roughness_ra_outer.setter
    def raceway_surface_roughness_ra_outer(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RacewaySurfaceRoughnessRaOuter = value

    @property
    def raceway_surface_roughness_rms_inner(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RacewaySurfaceRoughnessRMSInner' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RacewaySurfaceRoughnessRMSInner) if self.wrapped.RacewaySurfaceRoughnessRMSInner else None

    @raceway_surface_roughness_rms_inner.setter
    def raceway_surface_roughness_rms_inner(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RacewaySurfaceRoughnessRMSInner = value

    @property
    def raceway_surface_roughness_rms_outer(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'RacewaySurfaceRoughnessRMSOuter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.RacewaySurfaceRoughnessRMSOuter) if self.wrapped.RacewaySurfaceRoughnessRMSOuter else None

    @raceway_surface_roughness_rms_outer.setter
    def raceway_surface_roughness_rms_outer(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.RacewaySurfaceRoughnessRMSOuter = value

    @property
    def combined_surface_roughness_outer(self) -> 'float':
        '''float: 'CombinedSurfaceRoughnessOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CombinedSurfaceRoughnessOuter

    @property
    def combined_surface_roughness_inner(self) -> 'float':
        '''float: 'CombinedSurfaceRoughnessInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CombinedSurfaceRoughnessInner

    @property
    def number_of_elements(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfElements' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfElements) if self.wrapped.NumberOfElements else None

    @number_of_elements.setter
    def number_of_elements(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.TYPE
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.NumberOfElements = value

    @property
    def theoretical_maximum_number_of_elements(self) -> 'float':
        '''float: 'TheoreticalMaximumNumberOfElements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TheoreticalMaximumNumberOfElements

    @property
    def total_free_space_between_elements(self) -> 'float':
        '''float: 'TotalFreeSpaceBetweenElements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TotalFreeSpaceBetweenElements

    @property
    def free_space_between_elements(self) -> 'float':
        '''float: 'FreeSpaceBetweenElements' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.FreeSpaceBetweenElements

    @property
    def element_offset(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementOffset' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementOffset) if self.wrapped.ElementOffset else None

    @element_offset.setter
    def element_offset(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ElementOffset = value

    @property
    def distance_between_element_centres(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'DistanceBetweenElementCentres' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.DistanceBetweenElementCentres) if self.wrapped.DistanceBetweenElementCentres else None

    @distance_between_element_centres.setter
    def distance_between_element_centres(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.DistanceBetweenElementCentres = value

    @property
    def pitch_circle_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'PitchCircleDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.PitchCircleDiameter) if self.wrapped.PitchCircleDiameter else None

    @pitch_circle_diameter.setter
    def pitch_circle_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.PitchCircleDiameter = value

    @property
    def element_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ElementDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ElementDiameter) if self.wrapped.ElementDiameter else None

    @element_diameter.setter
    def element_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ElementDiameter = value

    @property
    def contact_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ContactAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ContactAngle) if self.wrapped.ContactAngle else None

    @contact_angle.setter
    def contact_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ContactAngle = value

    @property
    def load_ratio(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'LoadRatio' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.LoadRatio) if self.wrapped.LoadRatio else None

    @load_ratio.setter
    def load_ratio(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.LoadRatio = value

    @property
    def iso_material_factor(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ISOMaterialFactor' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ISOMaterialFactor) if self.wrapped.ISOMaterialFactor else None

    @iso_material_factor.setter
    def iso_material_factor(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ISOMaterialFactor = value

    @property
    def dynamic_capacity(self) -> 'float':
        '''float: 'DynamicCapacity' is the original name of this property.'''

        return self.wrapped.DynamicCapacity

    @dynamic_capacity.setter
    def dynamic_capacity(self, value: 'float'):
        self.wrapped.DynamicCapacity = float(value) if value else 0.0

    @property
    def dynamic_capacity_isots162812008(self) -> 'float':
        '''float: 'DynamicCapacityISOTS162812008' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DynamicCapacityISOTS162812008

    @property
    def static_capacity(self) -> 'float':
        '''float: 'StaticCapacity' is the original name of this property.'''

        return self.wrapped.StaticCapacity

    @static_capacity.setter
    def static_capacity(self, value: 'float'):
        self.wrapped.StaticCapacity = float(value) if value else 0.0

    @property
    def static_capacity_source(self) -> 'str':
        '''str: 'StaticCapacitySource' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StaticCapacitySource

    @property
    def dynamic_capacity_source(self) -> 'str':
        '''str: 'DynamicCapacitySource' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DynamicCapacitySource

    @property
    def dynamic_capacity_calculation(self) -> 'enum_with_selected_value.EnumWithSelectedValue_DynamicCapacityCalculationMethod':
        '''enum_with_selected_value.EnumWithSelectedValue_DynamicCapacityCalculationMethod: 'DynamicCapacityCalculation' is the original name of this property.'''

        return constructor.new(enum_with_selected_value.EnumWithSelectedValue_DynamicCapacityCalculationMethod)(self.wrapped.DynamicCapacityCalculation) if self.wrapped.DynamicCapacityCalculation else None

    @dynamic_capacity_calculation.setter
    def dynamic_capacity_calculation(self, value: 'enum_with_selected_value.EnumWithSelectedValue_DynamicCapacityCalculationMethod.implicit_type()'):
        wrapper_type = enum_with_selected_value.EnumWithSelectedValue_DynamicCapacityCalculationMethod.TYPE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicCapacityCalculationMethod.implicit_type()
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.DynamicCapacityCalculation = value

    @property
    def static_capacity_calculation(self) -> '_1486.StaticCapacityCalculationMethod':
        '''StaticCapacityCalculationMethod: 'StaticCapacityCalculation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.StaticCapacityCalculation)
        return constructor.new(_1486.StaticCapacityCalculationMethod)(value) if value else None

    @static_capacity_calculation.setter
    def static_capacity_calculation(self, value: '_1486.StaticCapacityCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.StaticCapacityCalculation = value

    @property
    def link_to_online_catalogue(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'LinkToOnlineCatalogue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LinkToOnlineCatalogue

    @property
    def extra_information(self) -> 'str':
        '''str: 'ExtraInformation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExtraInformation

    @property
    def type_information(self) -> '_1691.BearingTypeExtraInformation':
        '''BearingTypeExtraInformation: 'TypeInformation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.TypeInformation)
        return constructor.new(_1691.BearingTypeExtraInformation)(value) if value else None

    @property
    def is_skf_high_availability_item(self) -> 'bool':
        '''bool: 'IsSKFHighAvailabilityItem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsSKFHighAvailabilityItem

    @property
    def contact_radius_in_rolling_direction_inner(self) -> 'float':
        '''float: 'ContactRadiusInRollingDirectionInner' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactRadiusInRollingDirectionInner

    @property
    def contact_radius_in_rolling_direction_outer(self) -> 'float':
        '''float: 'ContactRadiusInRollingDirectionOuter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ContactRadiusInRollingDirectionOuter

    @property
    def cage_material(self) -> '_1462.BearingCageMaterial':
        '''BearingCageMaterial: 'CageMaterial' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.CageMaterial)
        return constructor.new(_1462.BearingCageMaterial)(value) if value else None

    @cage_material.setter
    def cage_material(self, value: '_1462.BearingCageMaterial'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.CageMaterial = value

    @property
    def sleeve_type(self) -> '_1700.SleeveType':
        '''SleeveType: 'SleeveType' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.SleeveType)
        return constructor.new(_1700.SleeveType)(value) if value else None

    @property
    def maximum_permissible_contact_stress_for_static_failure_inner(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MaximumPermissibleContactStressForStaticFailureInner' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MaximumPermissibleContactStressForStaticFailureInner) if self.wrapped.MaximumPermissibleContactStressForStaticFailureInner else None

    @maximum_permissible_contact_stress_for_static_failure_inner.setter
    def maximum_permissible_contact_stress_for_static_failure_inner(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MaximumPermissibleContactStressForStaticFailureInner = value

    @property
    def maximum_permissible_contact_stress_for_static_failure_outer(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'MaximumPermissibleContactStressForStaticFailureOuter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.MaximumPermissibleContactStressForStaticFailureOuter) if self.wrapped.MaximumPermissibleContactStressForStaticFailureOuter else None

    @maximum_permissible_contact_stress_for_static_failure_outer.setter
    def maximum_permissible_contact_stress_for_static_failure_outer(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.MaximumPermissibleContactStressForStaticFailureOuter = value

    @property
    def power_for_maximum_contact_stress_safety_factor(self) -> 'float':
        '''float: 'PowerForMaximumContactStressSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PowerForMaximumContactStressSafetyFactor

    @property
    def history(self) -> '_1264.FileHistory':
        '''FileHistory: 'History' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1264.FileHistory)(self.wrapped.History) if self.wrapped.History else None

    @property
    def protection(self) -> '_1688.BearingProtection':
        '''BearingProtection: 'Protection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1688.BearingProtection)(self.wrapped.Protection) if self.wrapped.Protection else None

    @property
    def element_material(self) -> '_233.BearingMaterial':
        '''BearingMaterial: 'ElementMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_233.BearingMaterial)(self.wrapped.ElementMaterial) if self.wrapped.ElementMaterial else None

    @property
    def inner_ring_material(self) -> '_233.BearingMaterial':
        '''BearingMaterial: 'InnerRingMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_233.BearingMaterial)(self.wrapped.InnerRingMaterial) if self.wrapped.InnerRingMaterial else None

    @property
    def outer_ring_material(self) -> '_233.BearingMaterial':
        '''BearingMaterial: 'OuterRingMaterial' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_233.BearingMaterial)(self.wrapped.OuterRingMaterial) if self.wrapped.OuterRingMaterial else None
