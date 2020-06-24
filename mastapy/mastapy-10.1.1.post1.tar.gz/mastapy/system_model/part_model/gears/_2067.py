'''_2067.py

FaceGear
'''


from mastapy.system_model.part_model.gears import _2070, _2069
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.gear_designs.face import _754
from mastapy._internal.python_net import python_net_import

_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGear',)


class FaceGear(_2069.Gear):
    '''FaceGear

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGear.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def orientation(self) -> '_2070.GearOrientations':
        '''GearOrientations: 'Orientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Orientation)
        return constructor.new(_2070.GearOrientations)(value) if value else None

    @orientation.setter
    def orientation(self, value: '_2070.GearOrientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def active_gear_design(self) -> '_754.FaceGearDesign':
        '''FaceGearDesign: 'ActiveGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_754.FaceGearDesign)(self.wrapped.ActiveGearDesign) if self.wrapped.ActiveGearDesign else None

    @property
    def face_gear_design(self) -> '_754.FaceGearDesign':
        '''FaceGearDesign: 'FaceGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_754.FaceGearDesign)(self.wrapped.FaceGearDesign) if self.wrapped.FaceGearDesign else None
