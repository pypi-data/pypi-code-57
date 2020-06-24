'''_648.py

PlungeShaverCalculationInputs
'''


from mastapy._internal.implicit import overridable
from mastapy._internal import constructor, conversion
from mastapy.gears import _305
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import _681
from mastapy.gears.gear_designs.cylindrical import _682, _683, _684
from mastapy._internal.cast_exception import CastException
from mastapy import _1
from mastapy._internal.python_net import python_net_import

_PLUNGE_SHAVER_CALCULATION_INPUTS = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving', 'PlungeShaverCalculationInputs')


__docformat__ = 'restructuredtext en'
__all__ = ('PlungeShaverCalculationInputs',)


class PlungeShaverCalculationInputs(_1.APIBase):
    '''PlungeShaverCalculationInputs

    This is a mastapy class.
    '''

    TYPE = _PLUNGE_SHAVER_CALCULATION_INPUTS
    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlungeShaverCalculationInputs.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def shaver_normal_module(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ShaverNormalModule' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ShaverNormalModule) if self.wrapped.ShaverNormalModule else None

    @shaver_normal_module.setter
    def shaver_normal_module(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ShaverNormalModule = value

    @property
    def shaver_normal_pressure_angle(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ShaverNormalPressureAngle' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ShaverNormalPressureAngle) if self.wrapped.ShaverNormalPressureAngle else None

    @shaver_normal_pressure_angle.setter
    def shaver_normal_pressure_angle(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ShaverNormalPressureAngle = value

    @property
    def thickness_at_diameter(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'ThicknessAtDiameter' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.ThicknessAtDiameter) if self.wrapped.ThicknessAtDiameter else None

    @thickness_at_diameter.setter
    def thickness_at_diameter(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.ThicknessAtDiameter = value

    @property
    def diameter_for_thickness(self) -> 'overridable.Overridable_float':
        '''overridable.Overridable_float: 'DiameterForThickness' is the original name of this property.'''

        return constructor.new(overridable.Overridable_float)(self.wrapped.DiameterForThickness) if self.wrapped.DiameterForThickness else None

    @diameter_for_thickness.setter
    def diameter_for_thickness(self, value: 'overridable.Overridable_float.implicit_type()'):
        wrapper_type = overridable.Overridable_float.TYPE
        enclosed_type = overridable.Overridable_float.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0.0)
        self.wrapped.DiameterForThickness = value

    @property
    def shaver_helix_angle(self) -> 'float':
        '''float: 'ShaverHelixAngle' is the original name of this property.'''

        return self.wrapped.ShaverHelixAngle

    @shaver_helix_angle.setter
    def shaver_helix_angle(self, value: 'float'):
        self.wrapped.ShaverHelixAngle = float(value) if value else 0.0

    @property
    def number_of_teeth_on_the_shaver(self) -> 'int':
        '''int: 'NumberOfTeethOnTheShaver' is the original name of this property.'''

        return self.wrapped.NumberOfTeethOnTheShaver

    @number_of_teeth_on_the_shaver.setter
    def number_of_teeth_on_the_shaver(self, value: 'int'):
        self.wrapped.NumberOfTeethOnTheShaver = int(value) if value else 0

    @property
    def shaver_hand(self) -> '_305.Hand':
        '''Hand: 'ShaverHand' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ShaverHand)
        return constructor.new(_305.Hand)(value) if value else None

    @shaver_hand.setter
    def shaver_hand(self, value: '_305.Hand'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ShaverHand = value

    @property
    def shaver_tip_diameter(self) -> 'float':
        '''float: 'ShaverTipDiameter' is the original name of this property.'''

        return self.wrapped.ShaverTipDiameter

    @shaver_tip_diameter.setter
    def shaver_tip_diameter(self, value: 'float'):
        self.wrapped.ShaverTipDiameter = float(value) if value else 0.0

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Name

    @property
    def input_gear_geometry(self) -> '_681.CylindricalCutterSimulatableGear':
        '''CylindricalCutterSimulatableGear: 'InputGearGeometry' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_681.CylindricalCutterSimulatableGear)(self.wrapped.InputGearGeometry) if self.wrapped.InputGearGeometry else None

    @property
    def tooth_thickness(self) -> '_682.ToothThicknessSpecificationBase':
        '''ToothThicknessSpecificationBase: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_682.ToothThicknessSpecificationBase)(self.wrapped.ToothThickness) if self.wrapped.ToothThickness else None

    @property
    def tooth_thickness_of_type_finish_tooth_thickness_design_specification(self) -> '_683.FinishToothThicknessDesignSpecification':
        '''FinishToothThicknessDesignSpecification: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ToothThickness.__class__.__qualname__ != 'FinishToothThicknessDesignSpecification':
            raise CastException('Failed to cast tooth_thickness to FinishToothThicknessDesignSpecification. Expected: {}.'.format(self.wrapped.ToothThickness.__class__.__qualname__))

        return constructor.new(_683.FinishToothThicknessDesignSpecification)(self.wrapped.ToothThickness) if self.wrapped.ToothThickness else None

    @property
    def tooth_thickness_of_type_tooth_thickness_specification(self) -> '_684.ToothThicknessSpecification':
        '''ToothThicknessSpecification: 'ToothThickness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if self.wrapped.ToothThickness.__class__.__qualname__ != 'ToothThicknessSpecification':
            raise CastException('Failed to cast tooth_thickness to ToothThicknessSpecification. Expected: {}.'.format(self.wrapped.ToothThickness.__class__.__qualname__))

        return constructor.new(_684.ToothThicknessSpecification)(self.wrapped.ToothThickness) if self.wrapped.ToothThickness else None
