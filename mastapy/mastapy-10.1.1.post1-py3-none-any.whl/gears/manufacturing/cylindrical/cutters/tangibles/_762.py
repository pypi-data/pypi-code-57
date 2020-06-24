'''_762.py

CutterShapeDefinition
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.manufacturing.cylindrical.cutters import (
    _751, _749, _750, _663,
    _736, _734, _717
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.cylindrical.cutters.tangibles import _768
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_CUTTER_SHAPE_DEFINITION = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles', 'CutterShapeDefinition')


__docformat__ = 'restructuredtext en'
__all__ = ('CutterShapeDefinition',)


class CutterShapeDefinition(_1.APIBase):
    '''CutterShapeDefinition

    This is a mastapy class.
    '''

    TYPE = _CUTTER_SHAPE_DEFINITION
    __hash__ = None

    def __init__(self, instance_to_wrap: 'CutterShapeDefinition.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def normal_module(self) -> 'float':
        '''float: 'NormalModule' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalModule

    @property
    def normal_pressure_angle(self) -> 'float':
        '''float: 'NormalPressureAngle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalPressureAngle

    @property
    def design(self) -> '_751.CylindricalGearRealCutterDesign':
        '''CylindricalGearRealCutterDesign: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_751.CylindricalGearRealCutterDesign)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_form_grinding_wheel(self) -> '_749.CylindricalGearFormGrindingWheel':
        '''CylindricalGearFormGrindingWheel: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Design.__class__.__qualname__ != 'CylindricalGearFormGrindingWheel':
            raise CastException('Failed to cast design to CylindricalGearFormGrindingWheel. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new(_749.CylindricalGearFormGrindingWheel)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_grinding_worm(self) -> '_750.CylindricalGearGrindingWorm':
        '''CylindricalGearGrindingWorm: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Design.__class__.__qualname__ != 'CylindricalGearGrindingWorm':
            raise CastException('Failed to cast design to CylindricalGearGrindingWorm. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new(_750.CylindricalGearGrindingWorm)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_hob_design(self) -> '_663.CylindricalGearHobDesign':
        '''CylindricalGearHobDesign: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Design.__class__.__qualname__ != 'CylindricalGearHobDesign':
            raise CastException('Failed to cast design to CylindricalGearHobDesign. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new(_663.CylindricalGearHobDesign)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_shaper(self) -> '_736.CylindricalGearShaper':
        '''CylindricalGearShaper: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Design.__class__.__qualname__ != 'CylindricalGearShaper':
            raise CastException('Failed to cast design to CylindricalGearShaper. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new(_736.CylindricalGearShaper)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_shaver(self) -> '_734.CylindricalGearShaver':
        '''CylindricalGearShaver: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Design.__class__.__qualname__ != 'CylindricalGearShaver':
            raise CastException('Failed to cast design to CylindricalGearShaver. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new(_734.CylindricalGearShaver)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def design_of_type_cylindrical_gear_plunge_shaver(self) -> '_717.CylindricalGearPlungeShaver':
        '''CylindricalGearPlungeShaver: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.Design.__class__.__qualname__ != 'CylindricalGearPlungeShaver':
            raise CastException('Failed to cast design to CylindricalGearPlungeShaver. Expected: {}.'.format(self.wrapped.Design.__class__.__qualname__))

        return constructor.new(_717.CylindricalGearPlungeShaver)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def fillet_points(self) -> 'List[_768.NamedPoint]':
        '''List[NamedPoint]: 'FilletPoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FilletPoints, constructor.new(_768.NamedPoint))
        return value

    @property
    def main_blade_points(self) -> 'List[_768.NamedPoint]':
        '''List[NamedPoint]: 'MainBladePoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MainBladePoints, constructor.new(_768.NamedPoint))
        return value
