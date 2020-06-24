'''_445.py

WormGearMeshDesign
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.worm import (
    _384, _702, _703, _475
)
from mastapy.gears.gear_designs import _946
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Worm', 'WormGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshDesign',)


class WormGearMeshDesign(_946.GearMeshDesign):
    '''WormGearMeshDesign

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def shaft_angle(self) -> 'float':
        '''float: 'ShaftAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaftAngle

    @property
    def centre_distance(self) -> 'float':
        '''float: 'CentreDistance' is the original name of this property.'''

        return self.wrapped.CentreDistance

    @centre_distance.setter
    def centre_distance(self, value: 'float'):
        self.wrapped.CentreDistance = float(value) if value else 0.0

    @property
    def standard_centre_distance(self) -> 'float':
        '''float: 'StandardCentreDistance' is the original name of this property.'''

        return self.wrapped.StandardCentreDistance

    @standard_centre_distance.setter
    def standard_centre_distance(self, value: 'float'):
        self.wrapped.StandardCentreDistance = float(value) if value else 0.0

    @property
    def wheel_addendum_modification_factor(self) -> 'float':
        '''float: 'WheelAddendumModificationFactor' is the original name of this property.'''

        return self.wrapped.WheelAddendumModificationFactor

    @wheel_addendum_modification_factor.setter
    def wheel_addendum_modification_factor(self, value: 'float'):
        self.wrapped.WheelAddendumModificationFactor = float(value) if value else 0.0

    @property
    def meshing_friction_angle(self) -> 'float':
        '''float: 'MeshingFrictionAngle' is the original name of this property.'''

        return self.wrapped.MeshingFrictionAngle

    @meshing_friction_angle.setter
    def meshing_friction_angle(self, value: 'float'):
        self.wrapped.MeshingFrictionAngle = float(value) if value else 0.0

    @property
    def coefficient_of_friction(self) -> 'float':
        '''float: 'CoefficientOfFriction' is the original name of this property.'''

        return self.wrapped.CoefficientOfFriction

    @coefficient_of_friction.setter
    def coefficient_of_friction(self, value: 'float'):
        self.wrapped.CoefficientOfFriction = float(value) if value else 0.0

    @property
    def worm_gear_set(self) -> '_384.WormGearSetDesign':
        '''WormGearSetDesign: 'WormGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_384.WormGearSetDesign)(self.wrapped.WormGearSet) if self.wrapped.WormGearSet else None

    @property
    def worm(self) -> '_702.WormDesign':
        '''WormDesign: 'Worm' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_702.WormDesign)(self.wrapped.Worm) if self.wrapped.Worm else None

    @property
    def wheel(self) -> '_703.WormWheelDesign':
        '''WormWheelDesign: 'Wheel' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_703.WormWheelDesign)(self.wrapped.Wheel) if self.wrapped.Wheel else None

    @property
    def worm_gears(self) -> 'List[_475.WormGearDesign]':
        '''List[WormGearDesign]: 'WormGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGears, constructor.new(_475.WormGearDesign))
        return value
