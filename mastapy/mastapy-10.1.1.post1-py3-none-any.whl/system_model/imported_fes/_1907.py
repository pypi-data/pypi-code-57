'''_1907.py

ImportedFELink
'''


from typing import List
from collections import OrderedDict

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy._internal.implicit import enum_with_selected_value, list_with_selected_item, overridable
from mastapy.system_model.imported_fes import (
    _1956, _1961, _1955, _1947
)
from mastapy.nodal_analysis.dev_tools_analyses import _1473
from mastapy.system_model.part_model import (
    _1989, _1982, _1985, _1987,
    _1992, _1993, _1996, _1998,
    _2001, _2004, _2005, _2006,
    _2008, _2010, _2012, _2013,
    _2018, _2019
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2022
from mastapy.system_model.part_model.gears import (
    _2052, _2054, _2056, _2057,
    _2058, _2060, _2062, _2064,
    _2066, _2067, _2069, _2073,
    _2075, _2077, _2079, _2082,
    _2084, _2086, _2088, _2089,
    _2090, _2092
)
from mastapy.system_model.part_model.couplings import (
    _2114, _2117, _2119, _2121,
    _2123, _2124, _2130, _2132,
    _2134, _2137, _2138, _2139,
    _2141, _2143
)
from mastapy.system_model.connections_and_sockets import (
    _1857, _1838, _1840, _1842,
    _1843, _1844, _1846, _1847,
    _1849, _1850, _1853, _1854,
    _1855
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1861, _1863, _1865, _1867,
    _1869, _1871, _1873, _1875,
    _1877, _1878, _1882, _1883,
    _1885, _1887, _1889, _1891,
    _1893
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1895, _1897, _1899, _1901,
    _1903, _1905, _1906
)
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_IMPORTED_FE_LINK = python_net_import('SMT.MastaAPI.SystemModel.ImportedFEs', 'ImportedFELink')


__docformat__ = 'restructuredtext en'
__all__ = ('ImportedFELink',)


class ImportedFELink(_0.APIBase):
    '''ImportedFELink

    This is a mastapy class.
    '''

    TYPE = _IMPORTED_FE_LINK

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ImportedFELink.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def external_node_i_ds(self) -> 'str':
        '''str: 'ExternalNodeIDs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ExternalNodeIDs

    @property
    def component_name(self) -> 'str':
        '''str: 'ComponentName' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ComponentName

    @property
    def connection(self) -> 'str':
        '''str: 'Connection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Connection

    @property
    def link_node_source(self) -> 'enum_with_selected_value.EnumWithSelectedValue_LinkNodeSource':
        '''enum_with_selected_value.EnumWithSelectedValue_LinkNodeSource: 'LinkNodeSource' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_LinkNodeSource.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.LinkNodeSource, value) if self.wrapped.LinkNodeSource else None

    @link_node_source.setter
    def link_node_source(self, value: 'enum_with_selected_value.EnumWithSelectedValue_LinkNodeSource.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LinkNodeSource.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value)
        self.wrapped.LinkNodeSource = value

    @property
    def link_to_get_nodes_from(self) -> 'list_with_selected_item.ListWithSelectedItem_ImportedFELink':
        '''list_with_selected_item.ListWithSelectedItem_ImportedFELink: 'LinkToGetNodesFrom' is the original name of this property.'''

        return constructor.new(list_with_selected_item.ListWithSelectedItem_ImportedFELink)(self.wrapped.LinkToGetNodesFrom) if self.wrapped.LinkToGetNodesFrom else None

    @link_to_get_nodes_from.setter
    def link_to_get_nodes_from(self, value: 'list_with_selected_item.ListWithSelectedItem_ImportedFELink.implicit_type()'):
        wrapper_type = list_with_selected_item.ListWithSelectedItem_ImportedFELink.wrapper_type()
        enclosed_type = list_with_selected_item.ListWithSelectedItem_ImportedFELink.implicit_type()
        value = wrapper_type[enclosed_type](value.wrapped if value else None)
        self.wrapped.LinkToGetNodesFrom = value

    @property
    def node_cylinder_search_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeCylinderSearchDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeCylinderSearchDiameter) if self.wrapped.NodeCylinderSearchDiameter else None

    @node_cylinder_search_diameter.setter
    def node_cylinder_search_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.NodeCylinderSearchDiameter = value

    @property
    def node_cone_search_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeConeSearchAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeConeSearchAngle) if self.wrapped.NodeConeSearchAngle else None

    @node_cone_search_angle.setter
    def node_cone_search_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.NodeConeSearchAngle = value

    @property
    def node_search_cylinder_thickness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeSearchCylinderThickness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeSearchCylinderThickness) if self.wrapped.NodeSearchCylinderThickness else None

    @node_search_cylinder_thickness.setter
    def node_search_cylinder_thickness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.NodeSearchCylinderThickness = value

    @property
    def node_cylinder_search_length(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeCylinderSearchLength' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeCylinderSearchLength) if self.wrapped.NodeCylinderSearchLength else None

    @node_cylinder_search_length.setter
    def node_cylinder_search_length(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.NodeCylinderSearchLength = value

    @property
    def node_cylinder_search_axial_offset(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'NodeCylinderSearchAxialOffset' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.NodeCylinderSearchAxialOffset) if self.wrapped.NodeCylinderSearchAxialOffset else None

    @node_cylinder_search_axial_offset.setter
    def node_cylinder_search_axial_offset(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.NodeCylinderSearchAxialOffset = value

    @property
    def number_of_nodes_in_ring(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfNodesInRing' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfNodesInRing) if self.wrapped.NumberOfNodesInRing else None

    @number_of_nodes_in_ring.setter
    def number_of_nodes_in_ring(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.NumberOfNodesInRing = value

    @property
    def has_teeth(self) -> 'bool':
        '''bool: 'HasTeeth' is the original name of this property.'''

        return self.wrapped.HasTeeth

    @has_teeth.setter
    def has_teeth(self, value: 'bool'):
        self.wrapped.HasTeeth = bool(value) if value else False

    @property
    def angle_of_centre_of_connection_patch(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'AngleOfCentreOfConnectionPatch' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.AngleOfCentreOfConnectionPatch) if self.wrapped.AngleOfCentreOfConnectionPatch else None

    @angle_of_centre_of_connection_patch.setter
    def angle_of_centre_of_connection_patch(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.AngleOfCentreOfConnectionPatch = value

    @property
    def span_of_patch(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'SpanOfPatch' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.SpanOfPatch) if self.wrapped.SpanOfPatch else None

    @span_of_patch.setter
    def span_of_patch(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.SpanOfPatch = value

    @property
    def node_selection_depth(self) -> 'overridable.Overridable_NodeSelectionDepthOption':
        '''overridable.Overridable_NodeSelectionDepthOption: 'NodeSelectionDepth' is the original name of this property.'''

        value = overridable.Overridable_NodeSelectionDepthOption.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.NodeSelectionDepth, value) if self.wrapped.NodeSelectionDepth else None

    @node_selection_depth.setter
    def node_selection_depth(self, value: 'overridable.Overridable_NodeSelectionDepthOption.implicit_type()'):
        wrapper_type = overridable.Overridable_NodeSelectionDepthOption.wrapper_type()
        enclosed_type = overridable.Overridable_NodeSelectionDepthOption.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.NodeSelectionDepth = value

    @property
    def coupling_type(self) -> 'overridable.Overridable_RigidCouplingType':
        '''overridable.Overridable_RigidCouplingType: 'CouplingType' is the original name of this property.'''

        value = overridable.Overridable_RigidCouplingType.wrapped_type()
        return enum_with_selected_value_runtime.create(self.wrapped.CouplingType, value) if self.wrapped.CouplingType else None

    @coupling_type.setter
    def coupling_type(self, value: 'overridable.Overridable_RigidCouplingType.implicit_type()'):
        wrapper_type = overridable.Overridable_RigidCouplingType.wrapper_type()
        enclosed_type = overridable.Overridable_RigidCouplingType.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.CouplingType = value

    @property
    def number_of_axial_nodes(self) -> 'int':
        '''int: 'NumberOfAxialNodes' is the original name of this property.'''

        return self.wrapped.NumberOfAxialNodes

    @number_of_axial_nodes.setter
    def number_of_axial_nodes(self, value: 'int'):
        self.wrapped.NumberOfAxialNodes = int(value) if value else 0

    @property
    def width_of_axial_patch(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'WidthOfAxialPatch' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.WidthOfAxialPatch) if self.wrapped.WidthOfAxialPatch else None

    @width_of_axial_patch.setter
    def width_of_axial_patch(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.WidthOfAxialPatch = value

    @property
    def connect_to_midside_nodes(self) -> 'bool':
        '''bool: 'ConnectToMidsideNodes' is the original name of this property.'''

        return self.wrapped.ConnectToMidsideNodes

    @connect_to_midside_nodes.setter
    def connect_to_midside_nodes(self, value: 'bool'):
        self.wrapped.ConnectToMidsideNodes = bool(value) if value else False

    @property
    def bearing_race_in_fe(self) -> 'overridable.Overridable_bool':
        '''overridable.Overridable_bool: 'BearingRaceInFE' is the original name of this property.'''

        return constructor.new(overridable.Overridable_bool)(self.wrapped.BearingRaceInFE) if self.wrapped.BearingRaceInFE else None

    @bearing_race_in_fe.setter
    def bearing_race_in_fe(self, value: 'overridable.Overridable_bool.implicit_type()'):
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else False)
        self.wrapped.BearingRaceInFE = value

    @property
    def number_of_nodes_in_full_fe_mesh(self) -> 'int':
        '''int: 'NumberOfNodesInFullFEMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfNodesInFullFEMesh

    @property
    def component(self) -> '_1989.Component':
        '''Component: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.Component)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_abstract_shaft_or_housing(self) -> '_1982.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.AbstractShaftOrHousing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1982.AbstractShaftOrHousing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bearing(self) -> '_1985.Bearing':
        '''Bearing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.Bearing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Bearing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1985.Bearing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bolt(self) -> '_1987.Bolt':
        '''Bolt: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.Bolt.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Bolt. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1987.Bolt)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_connector(self) -> '_1992.Connector':
        '''Connector: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.Connector.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Connector. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1992.Connector)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_datum(self) -> '_1993.Datum':
        '''Datum: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1993.Datum.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Datum. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1993.Datum)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_external_cad_model(self) -> '_1996.ExternalCADModel':
        '''ExternalCADModel: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.ExternalCADModel.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ExternalCADModel. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1996.ExternalCADModel)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_guide_dxf_model(self) -> '_1998.GuideDxfModel':
        '''GuideDxfModel: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.GuideDxfModel.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to GuideDxfModel. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_1998.GuideDxfModel)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_imported_fe_component(self) -> '_2001.ImportedFEComponent':
        '''ImportedFEComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.ImportedFEComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ImportedFEComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2001.ImportedFEComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_mass_disc(self) -> '_2004.MassDisc':
        '''MassDisc: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.MassDisc.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MassDisc. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2004.MassDisc)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_measurement_component(self) -> '_2005.MeasurementComponent':
        '''MeasurementComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.MeasurementComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MeasurementComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2005.MeasurementComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_mountable_component(self) -> '_2006.MountableComponent':
        '''MountableComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.MountableComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to MountableComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2006.MountableComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_oil_seal(self) -> '_2008.OilSeal':
        '''OilSeal: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2008.OilSeal.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to OilSeal. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2008.OilSeal)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_planet_carrier(self) -> '_2010.PlanetCarrier':
        '''PlanetCarrier: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.PlanetCarrier.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PlanetCarrier. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2010.PlanetCarrier)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_point_load(self) -> '_2012.PointLoad':
        '''PointLoad: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.PointLoad.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PointLoad. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2012.PointLoad)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_power_load(self) -> '_2013.PowerLoad':
        '''PowerLoad: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.PowerLoad.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PowerLoad. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2013.PowerLoad)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_unbalanced_mass(self) -> '_2018.UnbalancedMass':
        '''UnbalancedMass: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.UnbalancedMass.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to UnbalancedMass. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2018.UnbalancedMass)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_virtual_component(self) -> '_2019.VirtualComponent':
        '''VirtualComponent: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.VirtualComponent.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to VirtualComponent. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2019.VirtualComponent)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_shaft(self) -> '_2022.Shaft':
        '''Shaft: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.Shaft.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Shaft. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2022.Shaft)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_agma_gleason_conical_gear(self) -> '_2052.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.AGMAGleasonConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2052.AGMAGleasonConicalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_gear(self) -> '_2054.BevelDifferentialGear':
        '''BevelDifferentialGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.BevelDifferentialGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2054.BevelDifferentialGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_planet_gear(self) -> '_2056.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.BevelDifferentialPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2056.BevelDifferentialPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_differential_sun_gear(self) -> '_2057.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.BevelDifferentialSunGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2057.BevelDifferentialSunGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_bevel_gear(self) -> '_2058.BevelGear':
        '''BevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2058.BevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to BevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2058.BevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_concept_gear(self) -> '_2060.ConceptGear':
        '''ConceptGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.ConceptGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConceptGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2060.ConceptGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_conical_gear(self) -> '_2062.ConicalGear':
        '''ConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.ConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2062.ConicalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cylindrical_gear(self) -> '_2064.CylindricalGear':
        '''CylindricalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.CylindricalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CylindricalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2064.CylindricalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cylindrical_planet_gear(self) -> '_2066.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.CylindricalPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2066.CylindricalPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_face_gear(self) -> '_2067.FaceGear':
        '''FaceGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.FaceGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to FaceGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2067.FaceGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_gear(self) -> '_2069.Gear':
        '''Gear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.Gear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Gear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2069.Gear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_hypoid_gear(self) -> '_2073.HypoidGear':
        '''HypoidGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2073.HypoidGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to HypoidGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2073.HypoidGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2075.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2075.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2075.KlingelnbergCycloPalloidConicalGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2077.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2077.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2077.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2079.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2079.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_spiral_bevel_gear(self) -> '_2082.SpiralBevelGear':
        '''SpiralBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.SpiralBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2082.SpiralBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_diff_gear(self) -> '_2084.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.StraightBevelDiffGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2084.StraightBevelDiffGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_gear(self) -> '_2086.StraightBevelGear':
        '''StraightBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.StraightBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2086.StraightBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_planet_gear(self) -> '_2088.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.StraightBevelPlanetGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2088.StraightBevelPlanetGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_straight_bevel_sun_gear(self) -> '_2089.StraightBevelSunGear':
        '''StraightBevelSunGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.StraightBevelSunGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2089.StraightBevelSunGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_worm_gear(self) -> '_2090.WormGear':
        '''WormGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.WormGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to WormGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2090.WormGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_zerol_bevel_gear(self) -> '_2092.ZerolBevelGear':
        '''ZerolBevelGear: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2092.ZerolBevelGear.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2092.ZerolBevelGear)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_clutch_half(self) -> '_2114.ClutchHalf':
        '''ClutchHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.ClutchHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ClutchHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2114.ClutchHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_concept_coupling_half(self) -> '_2117.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2117.ConceptCouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2117.ConceptCouplingHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_coupling_half(self) -> '_2119.CouplingHalf':
        '''CouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2119.CouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2119.CouplingHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_cvt_pulley(self) -> '_2121.CVTPulley':
        '''CVTPulley: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2121.CVTPulley.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to CVTPulley. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2121.CVTPulley)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_part_to_part_shear_coupling_half(self) -> '_2123.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2123.PartToPartShearCouplingHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2123.PartToPartShearCouplingHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_pulley(self) -> '_2124.Pulley':
        '''Pulley: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2124.Pulley.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to Pulley. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2124.Pulley)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_rolling_ring(self) -> '_2130.RollingRing':
        '''RollingRing: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2130.RollingRing.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to RollingRing. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2130.RollingRing)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_shaft_hub_connection(self) -> '_2132.ShaftHubConnection':
        '''ShaftHubConnection: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2132.ShaftHubConnection.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2132.ShaftHubConnection)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_spring_damper_half(self) -> '_2134.SpringDamperHalf':
        '''SpringDamperHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2134.SpringDamperHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2134.SpringDamperHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_half(self) -> '_2137.SynchroniserHalf':
        '''SynchroniserHalf: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2137.SynchroniserHalf.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2137.SynchroniserHalf)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_part(self) -> '_2138.SynchroniserPart':
        '''SynchroniserPart: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2138.SynchroniserPart.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserPart. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2138.SynchroniserPart)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_synchroniser_sleeve(self) -> '_2139.SynchroniserSleeve':
        '''SynchroniserSleeve: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2139.SynchroniserSleeve.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2139.SynchroniserSleeve)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_torque_converter_pump(self) -> '_2141.TorqueConverterPump':
        '''TorqueConverterPump: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2141.TorqueConverterPump.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2141.TorqueConverterPump)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def component_of_type_torque_converter_turbine(self) -> '_2143.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'Component' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.TorqueConverterTurbine.TYPE not in self.wrapped.Component.__class__.__mro__:
            raise CastException('Failed to cast component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.Component.__class__.__qualname__))

        return constructor.new(_2143.TorqueConverterTurbine)(self.wrapped.Component) if self.wrapped.Component else None

    @property
    def socket(self) -> '_1857.Socket':
        '''Socket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1857.Socket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_cvt_pulley_socket(self) -> '_1838.CVTPulleySocket':
        '''CVTPulleySocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1838.CVTPulleySocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CVTPulleySocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1838.CVTPulleySocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_cylindrical_socket(self) -> '_1840.CylindricalSocket':
        '''CylindricalSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1840.CylindricalSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CylindricalSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1840.CylindricalSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_electric_machine_stator_socket(self) -> '_1842.ElectricMachineStatorSocket':
        '''ElectricMachineStatorSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1842.ElectricMachineStatorSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ElectricMachineStatorSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1842.ElectricMachineStatorSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_inner_shaft_connecting_socket(self) -> '_1843.InnerShaftConnectingSocket':
        '''InnerShaftConnectingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1843.InnerShaftConnectingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to InnerShaftConnectingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1843.InnerShaftConnectingSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_inner_shaft_socket(self) -> '_1844.InnerShaftSocket':
        '''InnerShaftSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1844.InnerShaftSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to InnerShaftSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1844.InnerShaftSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_outer_shaft_connecting_socket(self) -> '_1846.OuterShaftConnectingSocket':
        '''OuterShaftConnectingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1846.OuterShaftConnectingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to OuterShaftConnectingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1846.OuterShaftConnectingSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_outer_shaft_socket(self) -> '_1847.OuterShaftSocket':
        '''OuterShaftSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1847.OuterShaftSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to OuterShaftSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1847.OuterShaftSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_planetary_socket(self) -> '_1849.PlanetarySocket':
        '''PlanetarySocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1849.PlanetarySocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to PlanetarySocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1849.PlanetarySocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_pulley_socket(self) -> '_1850.PulleySocket':
        '''PulleySocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1850.PulleySocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to PulleySocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1850.PulleySocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_rolling_ring_socket(self) -> '_1853.RollingRingSocket':
        '''RollingRingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1853.RollingRingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to RollingRingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1853.RollingRingSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_shaft_connecting_socket(self) -> '_1854.ShaftConnectingSocket':
        '''ShaftConnectingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1854.ShaftConnectingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ShaftConnectingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1854.ShaftConnectingSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_shaft_socket(self) -> '_1855.ShaftSocket':
        '''ShaftSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1855.ShaftSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ShaftSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1855.ShaftSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_agma_gleason_conical_gear_teeth_socket(self) -> '_1861.AGMAGleasonConicalGearTeethSocket':
        '''AGMAGleasonConicalGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1861.AGMAGleasonConicalGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to AGMAGleasonConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1861.AGMAGleasonConicalGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_bevel_differential_gear_teeth_socket(self) -> '_1863.BevelDifferentialGearTeethSocket':
        '''BevelDifferentialGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1863.BevelDifferentialGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to BevelDifferentialGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1863.BevelDifferentialGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_bevel_gear_teeth_socket(self) -> '_1865.BevelGearTeethSocket':
        '''BevelGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1865.BevelGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to BevelGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1865.BevelGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_concept_gear_teeth_socket(self) -> '_1867.ConceptGearTeethSocket':
        '''ConceptGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1867.ConceptGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ConceptGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1867.ConceptGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_conical_gear_teeth_socket(self) -> '_1869.ConicalGearTeethSocket':
        '''ConicalGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1869.ConicalGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1869.ConicalGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_cylindrical_gear_teeth_socket(self) -> '_1871.CylindricalGearTeethSocket':
        '''CylindricalGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1871.CylindricalGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CylindricalGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1871.CylindricalGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_face_gear_teeth_socket(self) -> '_1873.FaceGearTeethSocket':
        '''FaceGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1873.FaceGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to FaceGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1873.FaceGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_gear_teeth_socket(self) -> '_1875.GearTeethSocket':
        '''GearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1875.GearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to GearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1875.GearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_hypoid_gear_teeth_socket(self) -> '_1877.HypoidGearTeethSocket':
        '''HypoidGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1877.HypoidGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to HypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1877.HypoidGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_klingelnberg_conical_gear_teeth_socket(self) -> '_1878.KlingelnbergConicalGearTeethSocket':
        '''KlingelnbergConicalGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1878.KlingelnbergConicalGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to KlingelnbergConicalGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1878.KlingelnbergConicalGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_klingelnberg_hypoid_gear_teeth_socket(self) -> '_1882.KlingelnbergHypoidGearTeethSocket':
        '''KlingelnbergHypoidGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1882.KlingelnbergHypoidGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to KlingelnbergHypoidGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1882.KlingelnbergHypoidGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_klingelnberg_spiral_bevel_gear_teeth_socket(self) -> '_1883.KlingelnbergSpiralBevelGearTeethSocket':
        '''KlingelnbergSpiralBevelGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1883.KlingelnbergSpiralBevelGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to KlingelnbergSpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1883.KlingelnbergSpiralBevelGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_spiral_bevel_gear_teeth_socket(self) -> '_1885.SpiralBevelGearTeethSocket':
        '''SpiralBevelGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1885.SpiralBevelGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to SpiralBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1885.SpiralBevelGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_straight_bevel_diff_gear_teeth_socket(self) -> '_1887.StraightBevelDiffGearTeethSocket':
        '''StraightBevelDiffGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1887.StraightBevelDiffGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to StraightBevelDiffGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1887.StraightBevelDiffGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_straight_bevel_gear_teeth_socket(self) -> '_1889.StraightBevelGearTeethSocket':
        '''StraightBevelGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1889.StraightBevelGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to StraightBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1889.StraightBevelGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_worm_gear_teeth_socket(self) -> '_1891.WormGearTeethSocket':
        '''WormGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1891.WormGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to WormGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1891.WormGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_zerol_bevel_gear_teeth_socket(self) -> '_1893.ZerolBevelGearTeethSocket':
        '''ZerolBevelGearTeethSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1893.ZerolBevelGearTeethSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ZerolBevelGearTeethSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1893.ZerolBevelGearTeethSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_clutch_socket(self) -> '_1895.ClutchSocket':
        '''ClutchSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1895.ClutchSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ClutchSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1895.ClutchSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_concept_coupling_socket(self) -> '_1897.ConceptCouplingSocket':
        '''ConceptCouplingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1897.ConceptCouplingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to ConceptCouplingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1897.ConceptCouplingSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_coupling_socket(self) -> '_1899.CouplingSocket':
        '''CouplingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1899.CouplingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to CouplingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1899.CouplingSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_part_to_part_shear_coupling_socket(self) -> '_1901.PartToPartShearCouplingSocket':
        '''PartToPartShearCouplingSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1901.PartToPartShearCouplingSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to PartToPartShearCouplingSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1901.PartToPartShearCouplingSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_spring_damper_socket(self) -> '_1903.SpringDamperSocket':
        '''SpringDamperSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1903.SpringDamperSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to SpringDamperSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1903.SpringDamperSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_torque_converter_pump_socket(self) -> '_1905.TorqueConverterPumpSocket':
        '''TorqueConverterPumpSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1905.TorqueConverterPumpSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to TorqueConverterPumpSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1905.TorqueConverterPumpSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def socket_of_type_torque_converter_turbine_socket(self) -> '_1906.TorqueConverterTurbineSocket':
        '''TorqueConverterTurbineSocket: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1906.TorqueConverterTurbineSocket.TYPE not in self.wrapped.Socket.__class__.__mro__:
            raise CastException('Failed to cast socket to TorqueConverterTurbineSocket. Expected: {}.'.format(self.wrapped.Socket.__class__.__qualname__))

        return constructor.new(_1906.TorqueConverterTurbineSocket)(self.wrapped.Socket) if self.wrapped.Socket else None

    @property
    def alignment_in_world_coordinate_system(self) -> '_1955.LinkComponentAxialPositionErrorReporter':
        '''LinkComponentAxialPositionErrorReporter: 'AlignmentInWorldCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1955.LinkComponentAxialPositionErrorReporter)(self.wrapped.AlignmentInWorldCoordinateSystem) if self.wrapped.AlignmentInWorldCoordinateSystem else None

    @property
    def alignment_in_fe_coordinate_system(self) -> '_1955.LinkComponentAxialPositionErrorReporter':
        '''LinkComponentAxialPositionErrorReporter: 'AlignmentInFECoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1955.LinkComponentAxialPositionErrorReporter)(self.wrapped.AlignmentInFECoordinateSystem) if self.wrapped.AlignmentInFECoordinateSystem else None

    @property
    def alignment_in_component_coordinate_system(self) -> '_1955.LinkComponentAxialPositionErrorReporter':
        '''LinkComponentAxialPositionErrorReporter: 'AlignmentInComponentCoordinateSystem' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1955.LinkComponentAxialPositionErrorReporter)(self.wrapped.AlignmentInComponentCoordinateSystem) if self.wrapped.AlignmentInComponentCoordinateSystem else None

    @property
    def nodes(self) -> 'List[_1947.ImportedFEStiffnessNode]':
        '''List[ImportedFEStiffnessNode]: 'Nodes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Nodes, constructor.new(_1947.ImportedFEStiffnessNode))
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def nodes_grouped_by_angle(self) -> 'OrderedDict[float, List[_1947.ImportedFEStiffnessNode]]':
        ''' 'NodesGroupedByAngle' is the original name of this method.

        Returns:
            OrderedDict[float, List[mastapy.system_model.imported_fes.ImportedFEStiffnessNode]]
        '''

        return conversion.pn_to_mp_objects_in_list_in_ordered_dict(self.wrapped.NodesGroupedByAngle(), constructor.new(_1947.ImportedFEStiffnessNode))

    def remove_all_nodes(self):
        ''' 'RemoveAllNodes' is the original name of this method.'''

        self.wrapped.RemoveAllNodes()

    def add_or_replace_node(self, node: '_1947.ImportedFEStiffnessNode'):
        ''' 'AddOrReplaceNode' is the original name of this method.

        Args:
            node (mastapy.system_model.imported_fes.ImportedFEStiffnessNode)
        '''

        self.wrapped.AddOrReplaceNode(node.wrapped if node else None)

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
