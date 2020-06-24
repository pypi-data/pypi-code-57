'''_571.py

ConicalMeshMicroGeometryConfigBase
'''


from mastapy.gears.manufacturing.bevel import (
    _562, _560, _561, _572,
    _573, _578
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.conical import _889
from mastapy.gears.gear_designs.zerol_bevel import _718
from mastapy.gears.gear_designs.straight_bevel_diff import _727
from mastapy.gears.gear_designs.straight_bevel import _731
from mastapy.gears.gear_designs.spiral_bevel import _735
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _739
from mastapy.gears.gear_designs.klingelnberg_hypoid import _743
from mastapy.gears.gear_designs.klingelnberg_conical import _747
from mastapy.gears.gear_designs.hypoid import _751
from mastapy.gears.gear_designs.bevel import _915
from mastapy.gears.gear_designs.agma_gleason_conical import _928
from mastapy.gears.analysis import _956
from mastapy._internal.python_net import python_net_import

_CONICAL_MESH_MICRO_GEOMETRY_CONFIG_BASE = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Bevel', 'ConicalMeshMicroGeometryConfigBase')


__docformat__ = 'restructuredtext en'
__all__ = ('ConicalMeshMicroGeometryConfigBase',)


class ConicalMeshMicroGeometryConfigBase(_956.GearMeshImplementationDetail):
    '''ConicalMeshMicroGeometryConfigBase

    This is a mastapy class.
    '''

    TYPE = _CONICAL_MESH_MICRO_GEOMETRY_CONFIG_BASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConicalMeshMicroGeometryConfigBase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def wheel_config(self) -> '_562.ConicalGearMicroGeometryConfigBase':
        '''ConicalGearMicroGeometryConfigBase: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_562.ConicalGearMicroGeometryConfigBase)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_gear_manufacturing_config(self) -> '_560.ConicalGearManufacturingConfig':
        '''ConicalGearManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _560.ConicalGearManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new(_560.ConicalGearManufacturingConfig)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_gear_micro_geometry_config(self) -> '_561.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _561.ConicalGearMicroGeometryConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new(_561.ConicalGearMicroGeometryConfig)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_pinion_manufacturing_config(self) -> '_572.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _572.ConicalPinionManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new(_572.ConicalPinionManufacturingConfig)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_pinion_micro_geometry_config(self) -> '_573.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _573.ConicalPinionMicroGeometryConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new(_573.ConicalPinionMicroGeometryConfig)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def wheel_config_of_type_conical_wheel_manufacturing_config(self) -> '_578.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'WheelConfig' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _578.ConicalWheelManufacturingConfig.TYPE not in self.wrapped.WheelConfig.__class__.__mro__:
            raise CastException('Failed to cast wheel_config to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.WheelConfig.__class__.__qualname__))

        return constructor.new(_578.ConicalWheelManufacturingConfig)(self.wrapped.WheelConfig) if self.wrapped.WheelConfig else None

    @property
    def mesh(self) -> '_889.ConicalGearMeshDesign':
        '''ConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_889.ConicalGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_zerol_bevel_gear_mesh_design(self) -> '_718.ZerolBevelGearMeshDesign':
        '''ZerolBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _718.ZerolBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to ZerolBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new(_718.ZerolBevelGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_straight_bevel_diff_gear_mesh_design(self) -> '_727.StraightBevelDiffGearMeshDesign':
        '''StraightBevelDiffGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _727.StraightBevelDiffGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to StraightBevelDiffGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new(_727.StraightBevelDiffGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_straight_bevel_gear_mesh_design(self) -> '_731.StraightBevelGearMeshDesign':
        '''StraightBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _731.StraightBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to StraightBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new(_731.StraightBevelGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_spiral_bevel_gear_mesh_design(self) -> '_735.SpiralBevelGearMeshDesign':
        '''SpiralBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _735.SpiralBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to SpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new(_735.SpiralBevelGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_design(self) -> '_739.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _739.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergCycloPalloidSpiralBevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new(_739.KlingelnbergCycloPalloidSpiralBevelGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_design(self) -> '_743.KlingelnbergCycloPalloidHypoidGearMeshDesign':
        '''KlingelnbergCycloPalloidHypoidGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _743.KlingelnbergCycloPalloidHypoidGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergCycloPalloidHypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new(_743.KlingelnbergCycloPalloidHypoidGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_klingelnberg_conical_gear_mesh_design(self) -> '_747.KlingelnbergConicalGearMeshDesign':
        '''KlingelnbergConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _747.KlingelnbergConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to KlingelnbergConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new(_747.KlingelnbergConicalGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_hypoid_gear_mesh_design(self) -> '_751.HypoidGearMeshDesign':
        '''HypoidGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _751.HypoidGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to HypoidGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new(_751.HypoidGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_bevel_gear_mesh_design(self) -> '_915.BevelGearMeshDesign':
        '''BevelGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _915.BevelGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to BevelGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new(_915.BevelGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None

    @property
    def mesh_of_type_agma_gleason_conical_gear_mesh_design(self) -> '_928.AGMAGleasonConicalGearMeshDesign':
        '''AGMAGleasonConicalGearMeshDesign: 'Mesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _928.AGMAGleasonConicalGearMeshDesign.TYPE not in self.wrapped.Mesh.__class__.__mro__:
            raise CastException('Failed to cast mesh to AGMAGleasonConicalGearMeshDesign. Expected: {}.'.format(self.wrapped.Mesh.__class__.__qualname__))

        return constructor.new(_928.AGMAGleasonConicalGearMeshDesign)(self.wrapped.Mesh) if self.wrapped.Mesh else None
