'''_957.py

FaceGearMeshMicroGeometry
'''


from typing import List

from mastapy.gears.gear_designs.face import _562, _969, _958
from mastapy._internal import constructor, conversion
from mastapy.gears.analysis import _717
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_MICRO_GEOMETRY = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Face', 'FaceGearMeshMicroGeometry')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshMicroGeometry',)


class FaceGearMeshMicroGeometry(_717.GearMeshImplementationDetail):
    '''FaceGearMeshMicroGeometry

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_MICRO_GEOMETRY
    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshMicroGeometry.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def face_mesh(self) -> '_562.FaceGearMeshDesign':
        '''FaceGearMeshDesign: 'FaceMesh' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_562.FaceGearMeshDesign)(self.wrapped.FaceMesh) if self.wrapped.FaceMesh else None

    @property
    def face_gear_set_micro_geometry(self) -> '_969.FaceGearSetMicroGeometry':
        '''FaceGearSetMicroGeometry: 'FaceGearSetMicroGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_969.FaceGearSetMicroGeometry)(self.wrapped.FaceGearSetMicroGeometry) if self.wrapped.FaceGearSetMicroGeometry else None

    @property
    def face_gear_micro_geometries(self) -> 'List[_958.FaceGearMicroGeometry]':
        '''List[FaceGearMicroGeometry]: 'FaceGearMicroGeometries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearMicroGeometries, constructor.new(_958.FaceGearMicroGeometry))
        return value
