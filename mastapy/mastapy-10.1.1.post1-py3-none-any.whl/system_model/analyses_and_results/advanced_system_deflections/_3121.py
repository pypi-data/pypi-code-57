'''_3121.py

GearAdvancedSystemDeflection
'''


from mastapy.system_model.part_model.gears import (
    _1989, _1980, _1984, _1987,
    _2010, _1993, _1974, _2002,
    _2004, _2006, _2012, _1976,
    _1977, _2008, _2009, _1997,
    _1999, _1986
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _3093
from mastapy._internal.python_net import python_net_import

_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'GearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GearAdvancedSystemDeflection',)


class GearAdvancedSystemDeflection(_3093.MountableComponentAdvancedSystemDeflection):
    '''GearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GEAR_ADVANCED_SYSTEM_DEFLECTION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1989.Gear':
        '''Gear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1989.Gear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear(self) -> '_1980.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ConceptGear':
            raise CastException('Failed to cast component_design to ConceptGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1980.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear(self) -> '_1984.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CylindricalGear':
            raise CastException('Failed to cast component_design to CylindricalGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1984.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear(self) -> '_1987.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'FaceGear':
            raise CastException('Failed to cast component_design to FaceGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1987.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear(self) -> '_2010.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'WormGear':
            raise CastException('Failed to cast component_design to WormGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2010.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear(self) -> '_1993.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'HypoidGear':
            raise CastException('Failed to cast component_design to HypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1993.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear(self) -> '_1974.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialGear':
            raise CastException('Failed to cast component_design to BevelDifferentialGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1974.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear(self) -> '_2002.SpiralBevelGear':
        '''SpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'SpiralBevelGear':
            raise CastException('Failed to cast component_design to SpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2002.SpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear(self) -> '_2004.StraightBevelDiffGear':
        '''StraightBevelDiffGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelDiffGear':
            raise CastException('Failed to cast component_design to StraightBevelDiffGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2004.StraightBevelDiffGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear(self) -> '_2006.StraightBevelGear':
        '''StraightBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelGear':
            raise CastException('Failed to cast component_design to StraightBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2006.StraightBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear(self) -> '_2012.ZerolBevelGear':
        '''ZerolBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'ZerolBevelGear':
            raise CastException('Failed to cast component_design to ZerolBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2012.ZerolBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_planet_gear(self) -> '_1976.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialPlanetGear':
            raise CastException('Failed to cast component_design to BevelDifferentialPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1976.BevelDifferentialPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_sun_gear(self) -> '_1977.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'BevelDifferentialSunGear':
            raise CastException('Failed to cast component_design to BevelDifferentialSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1977.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_planet_gear(self) -> '_2008.StraightBevelPlanetGear':
        '''StraightBevelPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelPlanetGear':
            raise CastException('Failed to cast component_design to StraightBevelPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2008.StraightBevelPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_sun_gear(self) -> '_2009.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'StraightBevelSunGear':
            raise CastException('Failed to cast component_design to StraightBevelSunGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2009.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear(self) -> '_1997.KlingelnbergCycloPalloidHypoidGear':
        '''KlingelnbergCycloPalloidHypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidHypoidGear':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1997.KlingelnbergCycloPalloidHypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear(self) -> '_1999.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'KlingelnbergCycloPalloidSpiralBevelGear':
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1999.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_planet_gear(self) -> '_1986.CylindricalPlanetGear':
        '''CylindricalPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ComponentDesign.__class__.__qualname__ != 'CylindricalPlanetGear':
            raise CastException('Failed to cast component_design to CylindricalPlanetGear. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1986.CylindricalPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
