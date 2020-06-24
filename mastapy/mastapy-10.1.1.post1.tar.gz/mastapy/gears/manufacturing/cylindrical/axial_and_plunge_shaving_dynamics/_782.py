'''_782.py

RedressingSettings
'''


from typing import Generic, TypeVar

from PIL.Image import Image

from mastapy._internal import constructor, conversion
from mastapy._internal.implicit import overridable
from mastapy.gears.manufacturing.cylindrical.cutters import _734
from mastapy import _1
from mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import _786
from mastapy._internal.python_net import python_net_import

_REDRESSING_SETTINGS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics', 'RedressingSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('RedressingSettings',)


T = TypeVar('T', bound='_786.ShavingDynamics')


class RedressingSettings(_1.APIBase, Generic[T]):
    '''RedressingSettings

    This is a mastapy class.

    Generic Types:
        T
    '''

    TYPE = _REDRESSING_SETTINGS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'RedressingSettings.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def selected(self) -> 'bool':
        '''bool: 'Selected' is the original name of this property.'''

        return self.wrapped.Selected

    @selected.setter
    def selected(self, value: 'bool'):
        self.wrapped.Selected = bool(value) if value else False

    @property
    def normal_thickness_at_reference_diameter(self) -> 'float':
        '''float: 'NormalThicknessAtReferenceDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalThicknessAtReferenceDiameter

    @property
    def shaver_tip_diameter(self) -> 'float':
        '''float: 'ShaverTipDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverTipDiameter

    @property
    def shaft_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ShaftAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ShaftAngle) if self.wrapped.ShaftAngle else None

    @shaft_angle.setter
    def shaft_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ShaftAngle = value

    @property
    def centre_distance(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'CentreDistance' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(overridable.Overridable_float)(self.wrapped.CentreDistance) if self.wrapped.CentreDistance else None

    @property
    def operating_normal_pressure_angle(self) -> 'float':
        '''float: 'OperatingNormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OperatingNormalPressureAngle

    @property
    def shaver_tip_thickness(self) -> 'float':
        '''float: 'ShaverTipThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverTipThickness

    @property
    def icon(self) -> 'Image':
        '''Image: 'Icon' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_image(self.wrapped.Icon)
        return value

    @property
    def shaving_status(self) -> 'str':
        '''str: 'ShavingStatus' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShavingStatus

    @property
    def shaver_minimum_sap_diameter(self) -> 'float':
        '''float: 'ShaverMinimumSAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverMinimumSAPDiameter

    @property
    def shaver_maximum_eap_diameter(self) -> 'float':
        '''float: 'ShaverMaximumEAPDiameter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ShaverMaximumEAPDiameter

    @property
    def redressed_shaver(self) -> '_734.CylindricalGearShaver':
        '''CylindricalGearShaver: 'RedressedShaver' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_734.CylindricalGearShaver)(self.wrapped.RedressedShaver) if self.wrapped.RedressedShaver else None
