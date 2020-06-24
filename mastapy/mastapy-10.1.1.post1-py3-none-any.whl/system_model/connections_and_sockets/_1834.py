'''_1834.py

ComponentConnection
'''


from typing import Callable

from PIL.Image import Image

from mastapy._internal import constructor, conversion
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
from mastapy.system_model.connections_and_sockets import _1835
from mastapy._internal.python_net import python_net_import

_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ComponentConnection')


__docformat__ = 'restructuredtext en'
__all__ = ('ComponentConnection',)


class ComponentConnection(_1835.ComponentMeasurer):
    '''ComponentConnection

    This is a mastapy class.
    '''

    TYPE = _COMPONENT_CONNECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ComponentConnection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def socket(self) -> 'str':
        '''str: 'Socket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Socket

    @property
    def connected_components_socket(self) -> 'str':
        '''str: 'ConnectedComponentsSocket' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ConnectedComponentsSocket

    @property
    def delete(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Delete' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Delete

    @property
    def assembly_view(self) -> 'Image':
        '''Image: 'AssemblyView' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_image(self.wrapped.AssemblyView)
        return value

    @property
    def detail_view(self) -> 'Image':
        '''Image: 'DetailView' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_image(self.wrapped.DetailView)
        return value

    @property
    def swap(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'Swap' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Swap

    @property
    def connected_component(self) -> '_1989.Component':
        '''Component: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.Component)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_abstract_shaft_or_housing(self) -> '_1982.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1982.AbstractShaftOrHousing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AbstractShaftOrHousing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1982.AbstractShaftOrHousing)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bearing(self) -> '_1985.Bearing':
        '''Bearing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.Bearing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Bearing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1985.Bearing)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bolt(self) -> '_1987.Bolt':
        '''Bolt: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.Bolt.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Bolt. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1987.Bolt)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_connector(self) -> '_1992.Connector':
        '''Connector: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1992.Connector.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Connector. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1992.Connector)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_datum(self) -> '_1993.Datum':
        '''Datum: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1993.Datum.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Datum. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1993.Datum)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_external_cad_model(self) -> '_1996.ExternalCADModel':
        '''ExternalCADModel: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.ExternalCADModel.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ExternalCADModel. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1996.ExternalCADModel)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_guide_dxf_model(self) -> '_1998.GuideDxfModel':
        '''GuideDxfModel: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.GuideDxfModel.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to GuideDxfModel. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_1998.GuideDxfModel)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_imported_fe_component(self) -> '_2001.ImportedFEComponent':
        '''ImportedFEComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2001.ImportedFEComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2001.ImportedFEComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_mass_disc(self) -> '_2004.MassDisc':
        '''MassDisc: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.MassDisc.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MassDisc. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2004.MassDisc)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_measurement_component(self) -> '_2005.MeasurementComponent':
        '''MeasurementComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2005.MeasurementComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MeasurementComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2005.MeasurementComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_mountable_component(self) -> '_2006.MountableComponent':
        '''MountableComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2006.MountableComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to MountableComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2006.MountableComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_oil_seal(self) -> '_2008.OilSeal':
        '''OilSeal: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2008.OilSeal.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to OilSeal. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2008.OilSeal)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_planet_carrier(self) -> '_2010.PlanetCarrier':
        '''PlanetCarrier: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2010.PlanetCarrier.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PlanetCarrier. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2010.PlanetCarrier)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_point_load(self) -> '_2012.PointLoad':
        '''PointLoad: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2012.PointLoad.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PointLoad. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2012.PointLoad)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_power_load(self) -> '_2013.PowerLoad':
        '''PowerLoad: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2013.PowerLoad.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PowerLoad. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2013.PowerLoad)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_unbalanced_mass(self) -> '_2018.UnbalancedMass':
        '''UnbalancedMass: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2018.UnbalancedMass.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to UnbalancedMass. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2018.UnbalancedMass)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_virtual_component(self) -> '_2019.VirtualComponent':
        '''VirtualComponent: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.VirtualComponent.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to VirtualComponent. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2019.VirtualComponent)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_shaft(self) -> '_2022.Shaft':
        '''Shaft: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2022.Shaft.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Shaft. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2022.Shaft)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_agma_gleason_conical_gear(self) -> '_2052.AGMAGleasonConicalGear':
        '''AGMAGleasonConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2052.AGMAGleasonConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to AGMAGleasonConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2052.AGMAGleasonConicalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_differential_gear(self) -> '_2054.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2054.BevelDifferentialGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2054.BevelDifferentialGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_differential_planet_gear(self) -> '_2056.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2056.BevelDifferentialPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2056.BevelDifferentialPlanetGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_differential_sun_gear(self) -> '_2057.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2057.BevelDifferentialSunGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2057.BevelDifferentialSunGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_bevel_gear(self) -> '_2058.BevelGear':
        '''BevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2058.BevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to BevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2058.BevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_concept_gear(self) -> '_2060.ConceptGear':
        '''ConceptGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2060.ConceptGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConceptGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2060.ConceptGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_conical_gear(self) -> '_2062.ConicalGear':
        '''ConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2062.ConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2062.ConicalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_cylindrical_gear(self) -> '_2064.CylindricalGear':
        '''CylindricalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2064.CylindricalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CylindricalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2064.CylindricalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_cylindrical_planet_gear(self) -> '_2066.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2066.CylindricalPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2066.CylindricalPlanetGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_face_gear(self) -> '_2067.FaceGear':
        '''FaceGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2067.FaceGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to FaceGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2067.FaceGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_gear(self) -> '_2069.Gear':
        '''Gear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2069.Gear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Gear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2069.Gear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_hypoid_gear(self) -> '_2073.HypoidGear':
        '''HypoidGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2073.HypoidGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to HypoidGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2073.HypoidGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_conical_gear(self) -> '_2075.KlingelnbergCycloPalloidConicalGear':
        '''KlingelnbergCycloPalloidConicalGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2075.KlingelnbergCycloPalloidConicalGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidConicalGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2075.KlingelnbergCycloPalloidConicalGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_2077.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2077.KlingelnbergCycloPalloidHypoidGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2077.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_2079.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2079.KlingelnbergCycloPalloidSpiralBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2079.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_spiral_bevel_gear(self) -> '_2082.SpiralBevelGear':
        '''SpiralBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2082.SpiralBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SpiralBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2082.SpiralBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_diff_gear(self) -> '_2084.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2084.StraightBevelDiffGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2084.StraightBevelDiffGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_gear(self) -> '_2086.StraightBevelGear':
        '''StraightBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2086.StraightBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2086.StraightBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_planet_gear(self) -> '_2088.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2088.StraightBevelPlanetGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2088.StraightBevelPlanetGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_straight_bevel_sun_gear(self) -> '_2089.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2089.StraightBevelSunGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2089.StraightBevelSunGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_worm_gear(self) -> '_2090.WormGear':
        '''WormGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2090.WormGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to WormGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2090.WormGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_zerol_bevel_gear(self) -> '_2092.ZerolBevelGear':
        '''ZerolBevelGear: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2092.ZerolBevelGear.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ZerolBevelGear. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2092.ZerolBevelGear)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_clutch_half(self) -> '_2114.ClutchHalf':
        '''ClutchHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2114.ClutchHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ClutchHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2114.ClutchHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_concept_coupling_half(self) -> '_2117.ConceptCouplingHalf':
        '''ConceptCouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2117.ConceptCouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ConceptCouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2117.ConceptCouplingHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_coupling_half(self) -> '_2119.CouplingHalf':
        '''CouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2119.CouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2119.CouplingHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_cvt_pulley(self) -> '_2121.CVTPulley':
        '''CVTPulley: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2121.CVTPulley.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to CVTPulley. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2121.CVTPulley)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_part_to_part_shear_coupling_half(self) -> '_2123.PartToPartShearCouplingHalf':
        '''PartToPartShearCouplingHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2123.PartToPartShearCouplingHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to PartToPartShearCouplingHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2123.PartToPartShearCouplingHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_pulley(self) -> '_2124.Pulley':
        '''Pulley: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2124.Pulley.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to Pulley. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2124.Pulley)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_rolling_ring(self) -> '_2130.RollingRing':
        '''RollingRing: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2130.RollingRing.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to RollingRing. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2130.RollingRing)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_shaft_hub_connection(self) -> '_2132.ShaftHubConnection':
        '''ShaftHubConnection: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2132.ShaftHubConnection.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to ShaftHubConnection. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2132.ShaftHubConnection)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_spring_damper_half(self) -> '_2134.SpringDamperHalf':
        '''SpringDamperHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2134.SpringDamperHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SpringDamperHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2134.SpringDamperHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_synchroniser_half(self) -> '_2137.SynchroniserHalf':
        '''SynchroniserHalf: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2137.SynchroniserHalf.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserHalf. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2137.SynchroniserHalf)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_synchroniser_part(self) -> '_2138.SynchroniserPart':
        '''SynchroniserPart: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2138.SynchroniserPart.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserPart. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2138.SynchroniserPart)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_synchroniser_sleeve(self) -> '_2139.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2139.SynchroniserSleeve.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to SynchroniserSleeve. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2139.SynchroniserSleeve)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_torque_converter_pump(self) -> '_2141.TorqueConverterPump':
        '''TorqueConverterPump: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2141.TorqueConverterPump.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to TorqueConverterPump. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2141.TorqueConverterPump)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None

    @property
    def connected_component_of_type_torque_converter_turbine(self) -> '_2143.TorqueConverterTurbine':
        '''TorqueConverterTurbine: 'ConnectedComponent' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2143.TorqueConverterTurbine.TYPE not in self.wrapped.ConnectedComponent.__class__.__mro__:
            raise CastException('Failed to cast connected_component to TorqueConverterTurbine. Expected: {}.'.format(self.wrapped.ConnectedComponent.__class__.__qualname__))

        return constructor.new(_2143.TorqueConverterTurbine)(self.wrapped.ConnectedComponent) if self.wrapped.ConnectedComponent else None
