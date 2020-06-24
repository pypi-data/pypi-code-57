'''_355.py

FaceGearSetDesign
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.face import (
    _602, _603, _962, _553,
    _516
)
from mastapy.gears.gear_designs import _353
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Face', 'FaceGearSetDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetDesign',)


class FaceGearSetDesign(_353.GearSetDesign):
    '''FaceGearSetDesign

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_DESIGN
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def shaft_angle(self) -> 'float':
        '''float: 'ShaftAngle' is the original name of this property.'''

        return self.wrapped.ShaftAngle

    @shaft_angle.setter
    def shaft_angle(self, value: 'float'):
        self.wrapped.ShaftAngle = float(value) if value else 0.0

    @property
    def nominal_pressure_angle(self) -> 'float':
        '''float: 'NominalPressureAngle' is the original name of this property.'''

        return self.wrapped.NominalPressureAngle

    @nominal_pressure_angle.setter
    def nominal_pressure_angle(self, value: 'float'):
        self.wrapped.NominalPressureAngle = float(value) if value else 0.0

    @property
    def working_normal_pressure_angle(self) -> 'float':
        '''float: 'WorkingNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WorkingNormalPressureAngle

    @property
    def module(self) -> 'float':
        '''float: 'Module' is the original name of this property.'''

        return self.wrapped.Module

    @module.setter
    def module(self, value: 'float'):
        self.wrapped.Module = float(value) if value else 0.0

    @property
    def normal_base_pitch(self) -> 'float':
        '''float: 'NormalBasePitch' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalBasePitch

    @property
    def pinion(self) -> '_602.FaceGearPinionDesign':
        '''FaceGearPinionDesign: 'Pinion' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_602.FaceGearPinionDesign)(self.wrapped.Pinion) if self.wrapped.Pinion else None

    @property
    def face_gear(self) -> '_603.FaceGearWheelDesign':
        '''FaceGearWheelDesign: 'FaceGear' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_603.FaceGearWheelDesign)(self.wrapped.FaceGear) if self.wrapped.FaceGear else None

    @property
    def cylindrical_gear_set_micro_geometry(self) -> '_962.FaceGearSetMicroGeometry':
        '''FaceGearSetMicroGeometry: 'CylindricalGearSetMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_962.FaceGearSetMicroGeometry)(self.wrapped.CylindricalGearSetMicroGeometry) if self.wrapped.CylindricalGearSetMicroGeometry else None

    @property
    def gears(self) -> 'List[_553.FaceGearDesign]':
        '''List[FaceGearDesign]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_553.FaceGearDesign))
        return value

    @property
    def face_gears(self) -> 'List[_553.FaceGearDesign]':
        '''List[FaceGearDesign]: 'FaceGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGears, constructor.new(_553.FaceGearDesign))
        return value

    @property
    def face_meshes(self) -> 'List[_516.FaceGearMeshDesign]':
        '''List[FaceGearMeshDesign]: 'FaceMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshes, constructor.new(_516.FaceGearMeshDesign))
        return value
